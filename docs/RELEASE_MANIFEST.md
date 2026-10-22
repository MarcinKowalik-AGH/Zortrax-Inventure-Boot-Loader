# Inventure boot v1.3 — binary release and publication scope

**Author:** Marcin Kowalik · mkowalik@agh.edu.pl  
**Publication:** 2026-10-22  
**Hardware:** verified Inventure V9, STM32F207, 256 KiB Flash  
**User-tested installation paths:** (A) from Inventure boot v1.2; (B) from **factory Zortrax bootloader v1.0**. Both resulted in a working original Zortrax application on tested printers.

## Distribution files expected

| Installation path | Installation card files |
| --- | --- |
| Existing v1.2 | `INVENTUR.IVB`, `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN` |
| Factory v1.0 | `InventureUpdate.bin`, `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN` |

A standalone **32-KiB** `Inventure_boot_v1.3_FULL_32KiB_0x08000000.bin` is for **SWD/ST-Link**, not an application updater. It cannot be installed by renaming it to `InventureUpdate.bin`.

The application restore image `RESTORE.BIN` is derived from original manufacturer firmware and is subject to rights separate from this third-party bootloader. **Do not redistribute proprietary manufacturer firmware without appropriate rights.** For a redistributable release, the user should supply their own compatible official image and verify its hash.

Test records from project work: **1099/1099** v1.3 offline tests, **11/11** installer tests, ARM integrity checks. The user has subsequently confirmed both installer paths on hardware. Other newly added v1.3 features (e.g. UART dumps, reset threshold and bulk backup) are not yet individually confirmed by a hardware test report.

## Security/privacy and source exclusion

**Only installation binaries authorized for redistribution and documentation are suitable for this public repository.** No C/ASM source, `.elf`, `.map`, build system, disassembly, cryptographic secrets, full 256-KiB printer dumps, NVM calibration, OTP, UID, option-byte snapshots, private backups, or internal reverse-engineering reports. No manufacturer firmware unless explicitly authorized for redistribution.

Never assume that a successful GitHub upload means a physical firmware update is risk-free. Replacing boot sectors carries an unavoidable power-loss risk and may require SWD recovery.

## Verified public SD release packages

The repository contains **both complete binary-only SD installation archives**, committed to public `main` under `SD_INSTALLATION/`. The uploaded ZIP Git object hashes were checked against the exact local archive bytes.

| Package | Archive | Bytes | ZIP SHA-256 | Git blob SHA-1 |
| --- | --- | ---: | --- | --- |
| v1.2 → v1.3 | [upgrade ZIP](../SD_INSTALLATION/01_UPGRADE_v1.2_to_v1.3/Inventure_boot_v1.3_SD_Z_v1.2_JEDNA_KARTA.zip) | 136276 | `1acb7a734263fd38046f89c4cb6e510454f69e5701885fa1d459f1f805e0ca9a` | `bd941135fcad1a37ff365369aeb599021050e1b9` |
| Factory v1.0 → v1.3 | [factory ZIP](../SD_INSTALLATION/02_FACTORY_ZORTRAX_v1.0_to_v1.3/Inventure_boot_v1.3_SD_FABRYCZNA_V9_JEDNA_KARTA.zip) | 151963 | `69e1c943284dd23d1cff71b07c6d57dea67d8cdeecc6df69a9045638ec017319` | `6bda427921aaf2c2968c6a8fe3c0f9bbbe0de28b` |

Each ZIP contains only its installer payload, `RESTORE.BIN` and two preallocated backup slots. No bootloader/installer source, ELF, map or private dump is included. The original Zortrax application payload in `RESTORE.BIN` remains subject to separate manufacturer rights and licensing.

For extraction, copy-to-SD steps, hardware checks, physical confirmation and restoring the application, see [bilingual SD installer guide](../SD_INSTALLATION/README.md).
