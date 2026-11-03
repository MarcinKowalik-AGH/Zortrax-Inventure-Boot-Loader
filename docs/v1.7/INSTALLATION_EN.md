# Zortrax Inventure boot v1.7 — FINAL (RELEASE 1.7)

Target: **Inventure V9 / STM32F207 / 256 KiB Flash**. Published: 3 November 2026. This exact build has not yet been hardware-accepted; the previous v1.5-HW2 was confirmed operational by its owner on one printer.

## P4 UART menu

Exactly five entries, **in this order**: **115200, 250000, 500000, 750000, 1500000**. 115200 comes first for compatibility, but the default is **250000 8N1**. `UART on bootwait` defaults to OFF, preventing Orange Pi startup probes from interrupting the five-second application autoboot. In ON mode, only a complete recognized diagnostic command after READY may interrupt. Persistent `P4-PERSIST-r3` settings use the reserved final 256 bytes of BOOT.

USART6 uses APB2 at nominal 24 MHz (HSI16 PLL, PLLM=16 PLLN=192 PLLP=8), OVER16 and BRR divisors **208, 96, 48, 32, 16** respectively. These yield nominal speeds **115384.615, 250000, 500000, 750000, 1500000**; the 115200 divider error is **+0.1603%**. They do not establish physical accuracy or host stability.

The stock r0323 font, read-only Hardware page, non-wrapping menu with pinned Back, differential OLED transfers, SD/serial APP updates, backup, recovery, logging, confirmation gestures and Flash layout are preserved. No M300 binaries or pin mapping were used.

## The three distinct downloads

- **SD_UPGRADE**: for a recognized previous custom bootloader. Extract `INVENTUR.IVB`, `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN` to the FAT32 root. The first install replaces APP with a temporary installer; in that installer take **two verified BOOT backups** before separately confirming BOOT replacement. Finish by explicitly restoring APP with `RESTORE.BIN` (manufacturer 1.6.1/r0323), or another separately verified application.
- **SD_FACTORY_V9**: only with a recognized factory V9 bootloader and compatible write/protection conditions. Contains `InventureUpdate.bin` instead of the IVB. The factory updater installs the temporary installer, after which the same backup / BOOT replacement / APP restoration workflow is mandatory.
- **STLINK**: a full 32768-byte boot image at `0x08000000`. Back up Flash first, program **only BOOT sectors 0–1**, then verify readback. Preserve all bytes at `0x08008000` and above; do not use Mass Erase, Read Unprotect or Option Byte changes.

Installer gestures: stock/custom APP install **OK+UP 2 s**; app launch **OK+DOWN 2 s**; the temporary BOOT installer has its own **release → OK press/release → OK+UP hold 5 s** confirmation. Replacing the entire BOOT resets P4 to 250000/OFF. `RESTORE.BIN` restores the stock APP, **not Klipper**; this release does not rebuild a compatible Klipper MCU or host.

## Validation and limitations

ARM linked BOOT size **32504 bytes**, **8 bytes free before the 256-byte settings journal**, full ST-Link file **32768 bytes**. Targeted P4/menu/UART tests **962/962 PASS**; both SD card structure checks PASS; shared BOOT target and original RESTORE verified. Full long-running regression suites exceeded the test execution limit, so no unsupported full-suite PASS is claimed. **Hardware acceptance of v1.7 remains pending.** See manifest and SHA256SUMS in firmware/v1.7. Previous firmware and manuals remain archived separately.
