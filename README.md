# Inventure boot v1.3 — Zortrax Inventure V9

**Independent, third-party service bootloader — firmware installation binaries and manuals.**  
**Author / Autor:** Marcin Kowalik · mkowalik@agh.edu.pl  
**Tested board / Testowana płyta:** Inventure V9, STM32F207, 256 KiB Flash.

[English installation manual](docs/INSTALLATION_EN.md) · [Instrukcja instalacji po polsku](docs/INSTALACJA_PL.md)  
[English features & UART commands](docs/FEATURES_AND_CONSOLE_EN.md) · [Funkcje i konsola po polsku](docs/FUNKCJE_I_KONSOLA_PL.md)  
[Release manifest & publication scope](docs/RELEASE_MANIFEST.md)

## Hardware status / Testy sprzętowe

**Confirmed by the project owner on physical printers:**

1. **Upgrade from Inventure boot v1.2 to v1.3 using SD.**
2. **Installation from original factory Zortrax bootloader v1.0 to Inventure boot v1.3 using SD**, followed by restoring and starting the original Zortrax application.

**Potwierdzono na rzeczywistych drukarkach:** oba scenariusze instalacji — aktualizację naszego v1.2 do v1.3 oraz instalację z fabrycznego bootloadera Zortrax v1.0. Po przywróceniu firmware fabryczna aplikacja uruchomiła się prawidłowo.

These tests validate both installation paths **on the tested printers**, not universal compatibility with all board versions or every advanced diagnostic feature.

## What it does / Funkcje

- **3-second interruptible autoboot** of a validated installed application; any front-panel key enters the maintenance menu.
- English OLED menu with UP / DOWN / OK navigation, **Back** on submenus and `© Marcin Kowalik` branding.
- Read, decrypt, verify and install compatible Zortrax firmware from FAT32 SD, with explicit confirmation.
- Avoid unnecessary rewrites when the selected firmware is already installed.
- Browse up to 16 update files on SD; checksum/progress feedback.
- Backup Flash/identity metadata to preallocated files; backup verification.
- Hardware diagnostics, reset reason and recovery latch, service-event history.
- UART6 service console at **250000 baud, 8N1**, including read-only information and binary memory export commands.
- Author information in OLED About / UART INFO.

## Installation variants

| Printer at the start | First-stage installer | Instructions |
| --- | --- | --- |
| Running **Inventure boot v1.2** | `INVENTUR.IVB` plus `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN` | [English](docs/INSTALLATION_EN.md) / [Polski](docs/INSTALACJA_PL.md) |
| Running **factory Zortrax bootloader v1.0** on verified V9 | `InventureUpdate.bin` plus the same other three files | [English](docs/INSTALLATION_EN.md) / [Polski](docs/INSTALACJA_PL.md) |

The first stage replaces the **application** with a service installer, the second stage saves and verifies two bootloader backups and installs new boot sectors, and the final stage restores an original compatible application. **A raw 32-KiB bootloader BIN is not an ordinary SD application update.**

## Downloads and redistribution

**No source code is published.** This repository is intended for binary installers that are legally redistributable, plus documentation. Do not upload C/ASM, ELF, maps, internal analyses, cryptographic secrets, printer Flash/NVM dumps, UID/OTP or proprietary manufacturer firmware without authorization.

> **Binary upload verification:** inspect the actual repository tree; the mere presence of this README does **not** imply installation ZIPs or BINs have already been released. A compatible original firmware image must be obtained lawfully from an appropriate source.

## Risks / Ryzyko

**Replacing bootloader sectors 0–1 is not power-loss-safe.** Losing power at the critical erase/program phase can require **ST-Link/SWD recovery**. Two backups on the same SD are not independent backups. Use stable power, confirmed motherboard identity and a recovery plan; never bypass unknown-hardware checks or use mass erase. The owner-tested installation paths do not justify assumptions about other Inventure board revisions.

Third-party project, not affiliated with or endorsed by Zortrax.
