# Installing Inventure boot v1.3 (English)

Author: **Marcin Kowalik** — mkowalik@agh.edu.pl

## Hardware validation

**Both installation routes have been tested successfully on physical Zortrax Inventure printers by the project owner:**
- Upgrade from an existing **Inventure boot v1.2** to **v1.3** using the SD service installer.
- Installation on a printer with the **original Zortrax bootloader v1.0**, followed by restoration and successful launch of the original application.

This validates the installation and boot path on the tested devices. It is **not** a blanket guarantee for every board revision or every diagnostic feature in v1.3. Supported reference hardware is Inventure **V9 / STM32F207 / 256 KiB Flash**. If your bootloader, flash size or motherboard differs, do not bypass compatibility checks.

## Download the correct one-card SD ZIP

Both downloadable packages are available in the public [SD_INSTALLATION folder](../SD_INSTALLATION/README.md).

- **For printers running Inventure boot v1.2:** [download upgrade v1.2 → v1.3 ZIP](../SD_INSTALLATION/01_UPGRADE_v1.2_to_v1.3/Inventure_boot_v1.3_SD_Z_v1.2_JEDNA_KARTA.zip) — SHA-256 `1acb7a734263fd38046f89c4cb6e510454f69e5701885fa1d459f1f805e0ca9a`.
- **For factory Zortrax bootloader v1.0 on verified V9:** [download factory v1.0 → v1.3 ZIP](../SD_INSTALLATION/02_FACTORY_ZORTRAX_v1.0_to_v1.3/Inventure_boot_v1.3_SD_FABRYCZNA_V9_JEDNA_KARTA.zip) — SHA-256 `69e1c943284dd23d1cff71b07c6d57dea67d8cdeecc6df69a9045638ec017319`.

Extract your ZIP **on your computer**, then copy the **four extracted files** into FAT32 SD root. The zip file itself must not remain as the only file on the SD card. For an end-to-end bilingual walkthrough see [SD_INSTALLATION/README.md](../SD_INSTALLATION/README.md).

## Choose exactly one installer

| Existing bootloader | First-stage file | Other SD files |
| --- | --- | --- |
| **Inventure boot v1.2** | `INVENTUR.IVB` | `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN` |
| **Factory Zortrax bootloader v1.0** (supported V9) | `InventureUpdate.bin` | `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN` |

Use the corresponding **binary-only SD installation package**. Format the card FAT32; copy all four files into its root directory, not into a subdirectory. Do not mix packages or rename the raw bootloader 32-KiB image to an update file. The `ZBACKUP` files are allocated **placeholders**, not valid backups until the installer has written and verified them.

The service installer temporarily replaces the printer's main application. `RESTORE.BIN` is the known original Inventure **1.6.1/r0323** application image used in project testing; ensure that your printer is compatible before applying it. Manufacturer firmware is subject to the manufacturer's intellectual-property rights and must be obtained lawfully.

## Route A — upgrade from Inventure boot v1.2

1. Confirm `INFO` identifies **v1.2**, check V9 motherboard, keep an independent backup and stable power. Have ST-Link/SWD recovery available if first-stage flash sectors are interrupted.
2. Insert the four-file **v1.2 upgrade** SD card. Press any button during the three-second countdown to enter the bootloader menu.
3. Select **Firmware on SD → Check SD package**. Confirm the result before proceeding.
4. Select **Install firmware**. Release all buttons; when prompted, hold **OK + UP for two seconds**. This first step installs the temporary **r9893 service application**, **not** v1.3 boot sectors.
5. Select **Start application / Launch application** (manual OK+DOWN confirmation), or let the existing bootloader start the service application. The display must identify **SD BOOT INSTALLER r9893**.
6. In the service installer select **Backup current boot x2**. It must write **and verify** both SD copies. Abort if a backup fails.
7. Select **Install new boot**. The installer checks both backups and original bootloader SHA before any erase. Approve the first confirmation with OK; after releasing the buttons, hold **OK + UP for five seconds** for final confirmation. DOWN cancels. This stage writes flash **sectors 0 and 1** and cannot be made power-failure-safe solely by SD backups.
8. After reset, interrupt the new v1.3 autoboot by pressing any key. **The service application is still installed**, so do not consider the task finished.
9. Use **Firmware on SD → Choose firmware file → RESTORE.BIN → Check selected file → Install selected file**. Confirm with **OK + UP for two seconds**. Do not inadvertently reinstall the service package that still exists on the card.
10. Run **VERIFY**, confirm expected application identity, then manually **BOOT**, or reset and permit automatic application start after three seconds. Confirm the native Zortrax menu works.

## Route B — factory Zortrax bootloader v1.0

1. Identify the motherboard as supported V9 and verify the factory bootloader image before modification. The verified reference 32-KiB SHA-256 is `19640ae302d918a79a243dbc7a5efcf055f78a1b459af4b50f3e66575af81752`. The installer refuses unrecognized images; **do not circumvent this check**.
2. Copy exactly `InventureUpdate.bin`, `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN` from the **factory v1.0** package to FAT32 root.
3. Insert SD and start the printer. The factory updater recognizes and installs the encrypted **r9893 service application** in the application area at `0x08010000`.
4. Once **SD BOOT INSTALLER r9893** starts, continue with steps **A6 through A10**: two verified bootloader backups, separately confirmed bootloader install, selection of `RESTORE.BIN`, verification, launch original application.

## Safety, rollback and memory map

| STM32 Flash | Role |
| --- | --- |
| `0x08000000–0x08007FFF` (sectors 0–1) | Bootloader, replaced by service installer |
| `0x08008000–0x0800FFFF` (sectors 2–3) | Factory NVM / settings, preserve |
| `0x08010000–0x0803FFFF` (sectors 4–5) | Application and metadata |

Do not mass-erase, change RDP/OTP/Option Bytes, disconnect power during flashing or try this on an unknown board. Two backup files on a **single SD card are not independent backups**. A corrupted first-stage bootloader may require SWD/ST-Link even if the card has copies. Neither the presence of an update file nor a normal reboot initiates an automatic app update: explicit menu and confirmation are required.

After installation: cancel countdown, run `INFO`, `VERIFY`, `SDCHECK`, `RESETINFO`; test **Back** navigation. With a validated application, a subsequent unattended startup should begin original firmware after three seconds.

See [features and console](FEATURES_AND_CONSOLE_EN.md).
