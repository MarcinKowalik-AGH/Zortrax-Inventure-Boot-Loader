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

## Current repository status

Documentation may be published before binary assets are uploaded. **Do not claim that the two installation ZIP packages or the standalone BIN are published until their GitHub object hashes and download URLs are verified.** See the actual repository tree for released artifacts.
