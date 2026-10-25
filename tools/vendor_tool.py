#!/usr/bin/env python3
"""Public, key-free Zortrax Inventure V9 application inspector and IVB packer.

* Accepts eight known ALREADY DECODED stock applications, identified by SHA-256.
* Preserves an already complete vendor payload only when its entire SHA-256
  equals an archived reference; never computes, guesses or exposes its tail.
* A raw app without a vendor tail can be wrapped as a CUSTOM-MANIFEST IVB;
  this is not a byte-identical recreation of the manufacturer's full payload.
* Encrypted ZRTX can be inspected at the OUTER-HEADER level only. Do not
  use this tool to decrypt it: use the bootloader's existing SD update route.
* Does not connect to hardware, modify option bytes, or change any input file.

Works with the companion tools/ibtool.py; Python standard library only.
No AES keys, signing keys, tail synthesis or decryption are supplied.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import sys
from typing import Optional

import ibtool

# Public *hashes*, not cryptographic keys or tail bytes.
# Entries describe archived Inventure V9 vendor images.
# Revision: (name, unpadded app size, unpadded app SHA-256,
#            complete canonical plaintext payload SHA-256).
KNOWN = {
    "r0155": ("1.2.0", 173948,
              "89a46c58b4633bb7cd5652aca1384333ad19d38ce51075bab58063d639a179b7",
              "fc19dd10ee995e0419d49a298d65fc4a9be561a6b0e16f77dc58012f35030596"),
    "r0207": ("1.2.1", 178192,
              "945aacf68ff849a279297bd769630ea6697c3110d896efdb747a9a19184b3ae7",
              "70e669104aa818c406aaef119620909b45b655f8235fbe9f699498a9f0e85769"),
    "r0219": ("1.2.2", 177964,
              "6ba46829accdf47edd9f7f28ba14288735cecdf019338034bd79372969d762df",
              "b4d178c9e62a41414ec87bc1f8eae0fc0d76eea0547058f746849dd87b9f523a"),
    "r0232": ("1.3.1", 178256,
              "d1f56d2a9c8dda419f815a1fbbbaed6a5b6f8e5f3fb9494d2713e6986ca0529b",
              "a3bb277311dc656bdfc24a37b02a1d0dbd07f3b57c39f4518c3142cf186b7cc8"),
    "r0279": ("1.4.0", 159500,
              "cd70b1744d6ce35edab7be775176a1a1af267b9853cb63f1e31ac443e7aa719a",
              "32beb402214dca94f1329bdfc1784e8a65779f8a4f8d59ab5a7e818851ccb344"),
    "r0300": ("1.5.1", 161392,
              "da3eeedf214df303869438ac88effc95091e0c2b311c0e9dc9d117f77518bb20",
              "ab4d6668d6e343e029e0e33e8f65ff52bdcd0a0f90e2be258bc844faca6f249e"),
    "r0309": ("1.5.4", 161552,
              "0acda824f55ddfdf926c84f968cdc093ce125b24fbbdfa7fbc05f4aba0ac4557",
              "2af5462f079822e6b9c1f3154b9ba79def839169b3f84b58e47414a3dd2c0baa"),
    "r0323": ("1.6.1", 164784,
              "9b980ba04531fac4425b77a23969076d24d8f25629fc2a501ac05d262c142268",
              "1368bdbddad941a8f7c025715946662a34d3def442d0d3c00af4315b54c8ba17"),
}


def inspect_and_normalize(blob: bytes) -> tuple[dict, Optional[bytes]]:
    if blob.startswith(ibtool.MAGIC):
        report = ibtool.inspect(blob)
        report.update(input_kind="IVB_ALREADY_PACKAGED", key_free=True)
        return report, blob

    # Inspection of vendor envelope metadata is deliberately not decryption.
    if blob.startswith(b"ZRTX"):
        if len(blob) < 21 or blob[:8] != b"ZRTXUINV":
            raise ValueError("Not an Inventure ZRTXUINV envelope")
        rev = blob[8:13].decode("ascii", errors="strict")
        if not re.fullmatch(r"r[0-9]{4}", rev):
            raise ValueError("Invalid vendor envelope revision")
        kind, length = struct.unpack_from("<II", blob, 13)
        if kind != 0xE1 or length < 64 or length % 64 or len(blob) != 21 + length:
            raise ValueError("Invalid or non-application ZRTX envelope")
        return {
            "input_kind": "ENCRYPTED_ZRTX_METADATA_ONLY",
            "revision_from_envelope": rev,
            "envelope_payload_bytes": length,
            "recognized_revision_label": rev in KNOWN,
            "content_authenticated": False,
            "ivb_export_supported": False,
            "next_step": "Use this supported ZRTX file with the custom bootloader SD update path (SDCHECK then SDUPDATE)",
        }, None

    if len(blob) < 44 or len(blob) > ibtool.LIMIT:
        raise ValueError("Expected an application image, not a full Flash dump or an unsupported file size")
    internal_magic, app_size = struct.unpack_from("<II", blob, 28)
    rev_bytes = blob[36:41]
    rev = rev_bytes.decode("ascii", errors="replace")
    if (internal_magic != 0x12345678 or not re.fullmatch(r"r[0-9]{4}", rev)
            or blob[41] != 0):
        raise ValueError("Not a recognized decoded vendor application header")
    row = KNOWN.get(rev)
    if row is None:
        raise ValueError("VENDOR_UNKNOWN_IMAGE: not an archived stock revision")
    name, expected_size, expected_sha, expected_full_sha = row
    if app_size != expected_size or app_size > len(blob):
        raise ValueError("VENDOR_UNKNOWN_IMAGE: application byte count mismatch")
    app = blob[:app_size]
    ibtool.validate_vectors(app)
    app_digest = hashlib.sha256(app).hexdigest()
    if app_digest != expected_sha:
        raise ValueError("VENDOR_UNKNOWN_IMAGE: application SHA-256 does not match the reference")

    normalized_payload = app
    form = "STOCK_APP_ONLY_CUSTOM_MANIFEST"
    preserves_vendor_full_payload = False
    if len(blob) != app_size:
        # No tail computation or HMAC signing. Accept only an *already existing*
        # vendor tail that produces an exact, previously archived full digest.
        padded_length = ((app_size + 20) // 64 + 1) * 64
        if len(blob) == app_size + 20:
            normalized_payload = blob + b"\xCD" * (padded_length - len(blob))
        elif len(blob) == padded_length:
            normalized_payload = blob
            if blob[app_size + 20:] != b"\xCD" * (padded_length - app_size - 20):
                raise ValueError("Invalid canonical padding")
        else:
            raise ValueError("Unsupported decoded stock length or missing vendor bytes")
        if hashlib.sha256(normalized_payload).hexdigest() != expected_full_sha:
            raise ValueError("Known vendor full-payload SHA-256 mismatch; no key or tail reconstruction available")
        form = "STOCK_COMPLETE_EXISTING_PAYLOAD_HASH_VERIFIED"
        preserves_vendor_full_payload = True

    ivb = ibtool.pack(normalized_payload)
    report = {
        "input_kind": form,
        "revision": rev,
        "software_version": name,
        "application_bytes": app_size,
        "wrapped_payload_bytes": len(normalized_payload),
        "application_sha256": app_digest,
        "wrapped_payload_sha256": hashlib.sha256(normalized_payload).hexdigest(),
        "preserves_vendor_full_payload": preserves_vendor_full_payload,
        "key_free": True,
        "notice": ("Existing full vendor payload verified by reference hash; no tail is derived"
                   if preserves_vendor_full_payload else
                   "Raw stock app wrapped as custom-manifest IVB without vendor tail; not an exact vendor-payload recreation"),
        "ivb": ibtool.inspect(ivb),
    }
    return report, ivb


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Known decoded stock APP, complete known plaintext, IVB, or ZRTX metadata")
    parser.add_argument("--ivb-out", type=Path, help="Write IVB, refusing existing output; unavailable for encrypted ZRTX")
    args = parser.parse_args()
    source = ibtool.read_bounded(args.input, ibtool.LIMIT + 21)
    report, ivb = inspect_and_normalize(source)
    if args.ivb_out:
        if ivb is None:
            raise ValueError("Encrypted ZRTX cannot be converted by the key-free public tool; install directly from SD, or supply your own already-decoded APP")
        with args.ivb_out.open("xb") as f:
            f.write(ivb)
            f.flush()
            os.fsync(f.fileno())
        report["created_ivb"] = str(args.ivb_out)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError) as exc:
        print("REJECTED: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
