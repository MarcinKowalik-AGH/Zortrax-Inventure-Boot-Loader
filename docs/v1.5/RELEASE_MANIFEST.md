# Inventure boot v1.5 — RELEASE 1.5-HW2: publication manifest

**Date:** 2026-10-29 · **Author:** Marcin Kowalik · **Target:** Inventure V9 / STM32F207 / 256 KiB.

[Project](../../README.md) · [PL installation](INSTALACJA_PL.md) · [EN installation](INSTALLATION_EN.md) · [v1.4 manifest retained](../v1.4/RELEASE_MANIFEST.md)

## Canonical artifacts — unchanged after the hardware report

| File | Bytes | SHA-256 |
|---|---:|---|
| [Inventure_boot_v1.5_HW2_STOCK_FONT_2026-10-29_SD_UPGRADE.zip](../../firmware/v1.5/Inventure_boot_v1.5_HW2_STOCK_FONT_2026-10-29_SD_UPGRADE.zip) | 140406 | `85640a127cd16fab1b24a8b8f69d3bf6c251865ab81df5223180a1ea8a209b85` |
| [Inventure_boot_v1.5_HW2_STOCK_FONT_2026-10-29_SD_FACTORY_V9.zip](../../firmware/v1.5/Inventure_boot_v1.5_HW2_STOCK_FONT_2026-10-29_SD_FACTORY_V9.zip) | 154971 | `3967bc324adfea5cfd374a5fbd1066877acece59f0f2d65be02fffd6326856e0` |
| [Inventure_boot_v1.5_HW2_STOCK_FONT_2026-10-29_STLINK_32KiB_0x08000000.bin](../../firmware/v1.5/Inventure_boot_v1.5_HW2_STOCK_FONT_2026-10-29_STLINK_32KiB_0x08000000.bin) | 32768 | `2d15e63a3db37bafb1f36d386d59b11c0d3d19f4d561b460b87e5201ab09b933` |

Both SD archives contain exactly four binary files: their installer, `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN`. The standalone BOOT is exactly 32768 bytes. The upgrade IVB contains this same BOOT. The factory and upgrade installer files match the preserved HW2 distribution. Do not substitute earlier v1.5 LARGE_FONT or UI-MEM1 artifacts.

`RESTORE.BIN`: 164864 bytes; SHA-256 `1368bdbddad941a8f7c025715946662a34d3def442d0d3c00af4315b54c8ba17`; fixed Zortrax APP 1.6.1/r0323, not a personal printer backup.

BOOT code/data: 32432 bytes, end `0x08007EB0`, 80 bytes spare before the 256-byte P4 journal at `0x08007F00`. Canonical BOOT padding/journal is FF. APP base `0x08010000`, NVM `0x08008000–0x0800FFFF`, boundaries unchanged. Installer APP body: 54660 bytes; transport envelope still uses r9898. Identify this release by hashes and `RELEASE 1.5-HW2`, not r9898 alone.

## Hardware status — updated after the original reports

**29 October 2026:** the owner reported in this project: “wgrałem na 1 drukarkę jest wszystko ok” (installed on one printer; everything works). This refers to the supplied **HW2** package. These published firmware files are not rebuilt or patched after that report.

This is one-printer owner feedback, not separately logged acceptance of all three routes, every baud rate, prolonged retention or power-loss recovery. The installer retains the pre-test literal `V1.5 HW2 - HW UNTESTED`; it describes the build-time state. Earlier private validation JSON/text still records `hardware_tested: false` and `github_changed: false` as historical build-time facts. Those historical fields are not silently rewritten as new test results.

**Hardware — potwierdzone na urządzeniu:** 29.10.2026 właściciel dodatkowo potwierdził, że ekran Hardware w stałym bootloaderze **poprawnie odczytuje rzeczywiste dane jego drukarki**. Nie jest to jedynie wynik testu modelowego. Ilustracje w instrukcji nadal zawierają jawnie syntetyczne dane przykładowe; nie są zrzutem prywatnych danych użytkownika.

**Hardware — physically confirmed:** on 29 October 2026 the owner explicitly confirmed that the permanent bootloader Hardware screen **correctly reads the actual printer data** on his device. This is an on-device confirmation, not just a model test. Manual previews still use clearly synthetic examples rather than private printer data.

## Recorded software evidence from the HW2 build

| Check | Recorded result | Scope |
|---|---:|---|
| BOOT native regression with production packed text | 3070 / 3070 | Native C with modeled HAL/memory/peripherals; no failures/errors/skips |
| Installer tests | 250 / 250 | Native/model control, backup, refusals, write flow and new UI/parser |
| ARM/ELF static checks | 99 / 99 | Memory/layout/vector/variant checks, not physical ARM execution |
| Original glyph comparison | 120 / 120 | Exact original r0323 bitmap widths and rows |
| Clean rebuild | 10 / 10 identical artifacts | Six BOOT BIN/ELF plus installer artifacts |
| Package parser comparisons | 12 + 12 | Current/previous parsers, simulated Flash |
| Renderer ASan/UBSan/bounds | 20000 iterations | Modeled text/progress/patterns and buffer boundaries |
| Hardware/text-decoder sanitizers | 20000 iterations | Synthetic OTP/NVM and malformed streams |

Counts overlap and are not added as independent hardware tests. Sources are the archived HW2 `BOOT_FINAL.xml`, `INSTALLER_FINAL.xml`, `REPRODUCIBILITY.json`, `FONT_DIRECT_STOCK.json` and associated logs. These private source archives are **not published**. This publication verifies deliverable byte identities, ZIP integrity, embedded target and links; it is not a new compiler or physical-printer test run.

## Differences from the preserved v1.4 publication

Original unscaled font in both programs; persistent read-only Hardware screen in BOOT and installer; non-wrapping stateful list movement; exact Back detection; dirty-rectangle OLED transfer; lossless text storage optimization. Flash geometry, APP formats, protection policy, P4 journal, backups, history, recovery and physical confirmation requirements remain.

`Hardware` reads model/profile, hardware/SN from Inventure OTP and **Print time** from NVM ID0. Missing/unreliable fields are independently `Unavailable`; valid zero is not replaced by missing-data text. Previews contain synthetic data only.

## Publication scope and archive

Only the three firmware distributions, checksums, updated descriptions/manuals and existing native PNG previews are added. Public key-free host utilities remain available. Only ibtool.py help wording was updated during the documentation audit; executable AST/protocol logic is unchanged. No standalone fonts, BOOT/installer source, ELF/map files, decryption/signing utilities, private complete ZIP or unique device dumps are uploaded.

The complete `firmware/v1.4`, its checksum file, versioned v1.4 manuals in docs/v1.4 and v1.3 archives remain. The v1.4 installer is **not promised to accept v1.5-HW2 as a downgrade source**.

## Documentation maintenance, 29 October 2026

Current documentation is fully contained in `docs/v1.5`; archived v1.4 manuals and their images are in `docs/v1.4`. Release binaries and the v1.5 tag are not changed. [Audit report](AUDYT_REPOZYTORIUM_PL.md) · [Machine-readable checks](AUDIT_CHECKS.json). Earlier build counts above are archived results, not a new firmware regression run.

### Current public host-tool identities

| File | SHA-256 | Change scope |
|---|---|---|
| [tools/ibtool.py](../../tools/ibtool.py) | `e68163fa90630aff4e330ef8368a16258a78616a52843348038e25fc4d849ab2` | Help text only; logic unchanged |
| [tools/vendor_tool.py](../../tools/vendor_tool.py) | `0c03dd74b4e763cf68b96325150bf01d2110a808a427e34fe8a792370cb377a8` | Byte-identical |
