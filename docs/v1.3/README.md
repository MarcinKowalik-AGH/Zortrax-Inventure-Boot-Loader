> **ARCHIWUM / ARCHIVE v1.3.** Historyczny przebieg instalacji, nie instrukcja bieżącego wydania. / Historical instructions, not the current release. [v1.5](../v1.5/README.md) · [Wersje / Versions](../README.md)

# Instalatory SD / SD installers

## Aktualne wydanie / Current version: v1.4 P4-PERSIST-r2

| Ścieżka / Route | Pobierz / Download |
|---|---|
| Własny rozpoznany BOOT / Existing recognized custom BOOT | [Inventure_boot_v1.4_P4_PERSIST_r2_SD_UPGRADE.zip](../../firmware/v1.4/Inventure_boot_v1.4_P4_PERSIST_r2_SD_UPGRADE.zip) |
| Fabryczny BOOT V9, RDP0 i zapisywalne BOOT/APP / Factory V9 with RDP0 and writable BOOT/APP | [Inventure_boot_v1.4_P4_PERSIST_r2_SD_FACTORY_V9.zip](../../firmware/v1.4/Inventure_boot_v1.4_P4_PERSIST_r2_SD_FACTORY_V9.zip) |

**[Instrukcja z ekranami po polsku](../v1.4/INSTALACJA_PL.md)** · **[Illustrated English manual](../v1.4/INSTALLATION_EN.md)**

Rozpakuj wybrany ZIP; na FAT32 skopiuj jego cztery pliki. **UPGRADE:** INVENTUR.IVB, RESTORE.BIN, ZBACKUP.BIN, ZBACK2.BIN. **FACTORY:** InventureUpdate.bin oraz te same trzy pozostałe nazwy. Nie mieszaj zestawów ani szablonów z rzeczywistymi wcześniejszymi kopiami.

Extract one ZIP; copy its four files to FAT32 root. Use the manual for the two backup files, separate BOOT confirmation and the mandatory application restore. The factory route does not disable protection.

ST-Link: [BIN 32 KiB](../../firmware/v1.4/Inventure_boot_v1.4_P4_PERSIST_r2_FULL_32KiB_0x08000000.bin) — tylko BOOT / BOOT only, **0x08000000**, sectors **0–1**. [Sumy kontrolne / Checksums](../../firmware/v1.4/SHA256SUMS.txt).

## Archiwum v1.3 / v1.3 archive

Poniższe pliki są wcześniejszym wydaniem, zachowanym bez zmian. Do nowej instalacji v1.4 użyj odnośników powyżej. / The following are unchanged historical files; use the links above for v1.4.

| Poprzedni pakiet / Historical package | Plik / File |
|---|---|
| v1.2 → v1.3 | [Inventure_boot_v1.3_SD_Z_v1.2_JEDNA_KARTA.zip](../../SD_INSTALLATION/01_UPGRADE_v1.2_to_v1.3/Inventure_boot_v1.3_SD_Z_v1.2_JEDNA_KARTA.zip) |
| Factory → v1.3 | [Inventure_boot_v1.3_SD_FABRYCZNA_V9_JEDNA_KARTA.zip](../../SD_INSTALLATION/02_FACTORY_ZORTRAX_v1.0_to_v1.3/Inventure_boot_v1.3_SD_FABRYCZNA_V9_JEDNA_KARTA.zip) |

Właściciel potwierdził w październiku 2026 działanie obu historycznych ścieżek v1.3 na drukarkach; potwierdzenie obecnej v1.4 jest zapisane w [manifeście](../v1.4/RELEASE_MANIFEST.md).
