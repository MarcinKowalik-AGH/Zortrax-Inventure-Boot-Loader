# Zortrax Inventure Boot Loader

**Latest: v1.7 FINAL — `RELEASE 1.7`** · Inventure V9 / STM32F207 / 256 KiB Flash. This build awaits physical validation; previous **v1.5-HW2** was tested on one printer. All versions remain archived.

## Downloads / Pobieranie

| Method | File |
|---|---|
| **UPGRADE** — recognized custom bootloader | [SD_UPGRADE](firmware/v1.7/Inventure_boot_v1.7_RELEASE_1.7_2026-11-03_SD_UPGRADE.zip) |
| **FROM FACTORY** — compatible original V9 bootloader | [SD_FACTORY_V9](firmware/v1.7/Inventure_boot_v1.7_RELEASE_1.7_2026-11-03_SD_FACTORY_V9.zip) |
| **ST-LINK** — 32 KiB at `0x08000000` | [STLINK](firmware/v1.7/Inventure_boot_v1.7_RELEASE_1.7_2026-11-03_STLINK_32KiB_0x08000000.bin) |

**UART rates, exactly:** 115200 · 250000 · 500000 · 750000 · 1500000. Default **250000/OFF**. P4-PERSIST-r3. 24 MHz USART6 clock and nominal dividers; see the guide for the 115200 error.

**[Polska instrukcja 1.7](docs/v1.7/INSTALACJA_PL.md) · [English manual 1.7](docs/v1.7/INSTALLATION_EN.md) · [SHA256](firmware/v1.7/SHA256SUMS.txt) · [Manifest](firmware/v1.7/MANIFEST.json)**

**Important:** SD installers replace APP temporarily; explicitly restore it after BOOT installation. The included `RESTORE.BIN` is **stock Zortrax 1.6.1/r0323**, not Klipper. Never use Mass Erase or unprotect procedures to bypass a refusal. Back up device-unique data first. ST-Link: BOOT sectors 0–1 only.

## Previous versions / Archiwum

- [v1.5-HW2 — owner-tested on one printer](docs/v1.5/README.md) · [firmware](firmware/v1.5)
- [v1.4 P4-PERSIST-r2](docs/v1.4/README.md) · [firmware](firmware/v1.4)
- [v1.3 historic SD cards](docs/v1.3/README.md)

[Documentation index](docs/README.md) · [Public key-free host tools](tools/README.md). No private vendor keys, confidential firmware sources, unique printer data or tail20 creation code are published.
