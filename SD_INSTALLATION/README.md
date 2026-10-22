# SD installation packages — Inventure boot v1.3

**Author:** Marcin Kowalik · mkowalik@agh.edu.pl  
**Tested hardware:** Zortrax Inventure V9, STM32F207, 256 KiB Flash.  
**Status:** Both installation paths **successfully tested on physical printers** by the project owner: v1.2 upgrade and factory Zortrax bootloader v1.0.

Choose ONE package, download its ZIP, extract the files, and copy those files to the **root of a FAT32 SD card**. Do not copy the ZIP itself to the card.

| Printer currently running | Download ZIP | First stage |
| --- | --- | --- |
| **Inventure boot v1.2** | [01_UPGRADE_v1.2_to_v1.3](01_UPGRADE_v1.2_to_v1.3/Inventure_boot_v1.3_SD_Z_v1.2_JEDNA_KARTA.zip) | `INVENTUR.IVB` |
| **Factory Zortrax bootloader v1.0** on supported V9 | [02_FACTORY_ZORTRAX_v1.0_to_v1.3](02_FACTORY_ZORTRAX_v1.0_to_v1.3/Inventure_boot_v1.3_SD_FABRYCZNA_V9_JEDNA_KARTA.zip) | `InventureUpdate.bin` |

## Files after extracting

**Upgrade v1.2:** `INVENTUR.IVB`, `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN`.

**Factory v1.0:** `InventureUpdate.bin`, `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN`.

The two `ZBACKUP` files are **empty allocated backup slots** before use. They only become valid after the service installer writes and checks the printer's existing bootloader. `RESTORE.BIN` is the known original application **1.6.1/r0323** used in hardware tests; before installation, verify this is compatible with the target printer and respect the manufacturer's firmware license.

## EN — step-by-step

### 1. Upgrade from Inventure boot v1.2

1. Verify you have v1.2 in `INFO`, confirm compatible V9 motherboard, use stable power and preserve a separate copy of the original settings/firmware. Keep SWD/ST-Link recovery available.
2. Download and unzip the **01_UPGRADE** archive above; copy its four files to FAT32 SD root.
3. Insert card and press any key during the **3-second autoboot countdown** to enter the bootloader menu.
4. In **Firmware on SD**, run **Check SD package** for `INVENTUR.IVB`; then **Install firmware** and confirm with **OK+UP held for 2 seconds**. This installs a **temporary r9893 service application**, not the new bootloader yet.
5. Launch the service application by **BOOT / Start application**, confirming **OK+DOWN for 2 seconds** as prompted.
6. In the **SD BOOT INSTALLER r9893** menu run **Backup current boot x2**. Confirm successful write-and-readback of both copies.
7. Select **Install new boot**. Release buttons, accept the first OK confirmation, then hold **OK+UP for 5 seconds** for the final authorization. **This erases and writes sectors 0–1**; never interrupt power.
8. On restart, press any key to enter **Inventure boot v1.3** service menu. The temporary service application still occupies application Flash.
9. Use **Firmware on SD → Choose firmware file → RESTORE.BIN**, validate it, then choose **Install selected file** and confirm **OK+UP for 2 seconds**. Do not reinstall the service application.
10. Run `VERIFY`, then `BOOT` with confirmation, or reset and allow the three-second autoboot. Confirm the normal Zortrax menu starts.

### 2. Factory Zortrax bootloader v1.0

1. Confirm a **supported V9 board** with the factory bootloader recognized by the installer. Do not override the compatibility lock.
2. Download and unzip **02_FACTORY**; copy its four files to FAT32 SD root.
3. Insert SD and start the printer: the original factory update mechanism installs the encrypted `InventureUpdate.bin` **temporary service application r9893**.
4. From **SD BOOT INSTALLER r9893** run **Backup current boot x2**, then **Install new boot** with the two confirmations above.
5. After reboot, enter new **Inventure boot v1.3**, select **RESTORE.BIN**, install/verify the original application and boot it, as in steps 8–10 of the upgrade instructions.

## PL — krok po kroku

### 1. Aktualizacja naszego bootloadera v1.2 do v1.3

1. Potwierdź przez `INFO` wersję v1.2 oraz zgodną płytę V9. Zachowaj niezależną kopię pamięci i możliwość ratowania przez ST-Link.
2. Pobierz ZIP **01_UPGRADE**, rozpakuj i skopiuj **cztery pliki** do głównego katalogu karty FAT32.
3. Włóż kartę i naciśnij dowolny przycisk podczas trzysekundowego autostartu.
4. W menu **Firmware on SD** sprawdź `INVENTUR.IVB`, następnie wybierz aktualizację aplikacji i potwierdź **OK+GÓRA przez 2 sekundy**. To zapisze **tymczasowy instalator r9893**.
5. Uruchom zainstalowaną aplikację serwisową poleceniem **BOOT / Start application**, potwierdzając **OK+DÓŁ przez 2 sekundy**.
6. W menu **SD BOOT INSTALLER r9893** wybierz **Backup current boot x2** i zaczekaj na poprawną weryfikację **obu** kopii.
7. Wybierz **Install new boot**; po zwolnieniu przycisków potwierdź OK, a następnie **OK+GÓRA przez 5 sekund**. Programuje to sektory **0–1** — zasilanie musi być nieprzerwane.
8. Po restarcie przerwij autostart nowego **Inventure boot v1.3**, wejdź w **Firmware on SD → Choose firmware file → RESTORE.BIN** i sprawdź plik.
9. Wybierz **Install selected file**, potwierdź **OK+GÓRA przez 2 sekundy**.
10. Wykonaj `VERIFY`, następnie `BOOT` lub restart z autostartem po 3 sekundach. Powinno działać oryginalne menu Zortraxa.

### 2. Fabryczny bootloader Zortraxa v1.0

1. Sprawdź zgodność płyty **V9** i wersję fabryczną bootloadera. Nie omijaj blokady nierozpoznanego kodu.
2. Pobierz ZIP **02_FACTORY**, rozpakuj i skopiuj cztery pliki na FAT32.
3. Fabryczny aktualizator po uruchomieniu wgra `InventureUpdate.bin` jako **tymczasową aplikację r9893**.
4. W **SD BOOT INSTALLER** wykonaj **Backup current boot x2** i **Install new boot** z oddzielnym potwierdzeniem.
5. W nowym v1.3 wybierz i wgraj **RESTORE.BIN**, uruchom `VERIFY`, następnie `BOOT` lub autostart, jak w procedurze upgrade.

## Integrity / Sumy kontrolne ZIP (SHA-256)

| Package | ZIP bytes | SHA-256 |
| --- | ---: | --- |
| v1.2 → v1.3 | 136276 | `1acb7a734263fd38046f89c4cb6e510454f69e5701885fa1d459f1f805e0ca9a` |
| factory v1.0 → v1.3 | 151963 | `69e1c943284dd23d1cff71b07c6d57dea67d8cdeecc6df69a9045638ec017319` |

On Mac: `shasum -a 256 <downloaded.zip>`; in Linux: `sha256sum <downloaded.zip>`.

## Critical safety / Bezpieczeństwo

Bootloader installation changes **STM32 flash sectors 0–1**; a power failure may require **ST-Link/SWD recovery**. The service application temporarily replaces the original application. The factory NVM calibration area must not be erased. Two backup slots on **one SD card are not independent backups**. Do not use on an unknown board revision, skip compatibility checks, modify OTP/RDP/Option Bytes, or mass erase.

The package contains an original application payload for restoration, which is subject to Zortrax copyright/licensing. Redistribution/use is subject to applicable rights.

**Complete manuals / Szczegółowe instrukcje:**
[English](../docs/INSTALLATION_EN.md) · [Polski](../docs/INSTALACJA_PL.md) · [Features / UART English](../docs/FEATURES_AND_CONSOLE_EN.md) · [Funkcje / UART po polsku](../docs/FUNKCJE_I_KONSOLA_PL.md).
