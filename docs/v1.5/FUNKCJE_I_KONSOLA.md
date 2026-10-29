# Inventure v1.5-HW2 — funkcje, Hardware i konsola / features and console

[Projekt / Project](../../README.md) · [Instrukcja PL](INSTALACJA_PL.md) · [EN installation](INSTALLATION_EN.md) · [Przykłady APP / APP examples](P4_EXAMPLES.md)

**Hardware — potwierdzone na urządzeniu:** 29.10.2026 właściciel dodatkowo potwierdził, że ekran Hardware w stałym bootloaderze **poprawnie odczytuje rzeczywiste dane jego drukarki**. Nie jest to jedynie wynik testu modelowego. Ilustracje w instrukcji nadal zawierają jawnie syntetyczne dane przykładowe; nie są zrzutem prywatnych danych użytkownika.

**Hardware — physically confirmed:** on 29 October 2026 the owner explicitly confirmed that the permanent bootloader Hardware screen **correctly reads the actual printer data** on his device. This is an on-device confirmation, not just a model test. Manual previews still use clearly synthetic examples rather than private printer data.

## Wygląd i nawigacja / Display and navigation

BOOT i instalator korzystają z oryginalnych bitmap r0323 **bez skalowania**. Nagłówek: `Inventure boot v1.5 © Marcin Kowalik`. Menu główne ma cztery widoczne wiersze; podmenu ma przypięty Back i trzy przewijane pozycje. Koniec/początek listy nie zawija. Zmiana kierunku najpierw przesuwa wskaźnik w obecnym oknie. Lista plików normalizuje indeksy po zmianie długości. Pierwsza klatka OLED jest pełna, kolejne przesyłają zmieniony prostokąt, identyczna — zero danych.

Both programs use the original unscaled font. Lists stop at boundaries, remember their viewport and distinguish Back from Backup. A first full display transfer is followed by changed-rectangle updates. Model tests of transfer size are not a physical latency/flicker measurement.

![Interfejs i odczyt pamięci](../images/v1.5/overview.png)

*Rendery C, nie fotografie; dane egzemplarza są syntetyczne. / Native renders, not photos; device data are synthetic.*

## Menu stałego BOOT / Permanent BOOT menu

| Główna pozycja / Main entry | Podmenu / Entries after Back |
|---|---|
| Start application | Launch application |
| Firmware on SD | Check SD package; Install firmware; Choose firmware file |
| Diagnostics | Verify Flash; Hardware; Reset / Recovery; Clear recovery lock; Buttons / raw inputs; Display test; UART; SD card info |
| About | © Marcin Kowalik; mkowalik@agh.edu.pl; Version v1.5 |
| Restart | Restart controller |
| Backup Flash | Backup Flash + identity |
| Service history | View history on UART; Save history to SD |

`Diagnostics → UART`: Back, UART test, P4 baud rate. Baud: Back, 19200, 57600, 115200, 250000, 500000. Przeglądarka / browser: Back plus up to 16 root BIN/IVB files; selected-file page: Back to files, Check selected file, Install selected file. Selection is not verification.

## Hardware — odczyt, nie test zapisu / read-only device information

Stały BOOT: `Diagnostics → Hardware`. Pośrednik: `Hardware`.

```text
Model: Zortrax Inventure
Hardware version: <two-digit OTP value>
Serial number: <Z plus eight hexadecimal digits>
Print time: <hours>h <minutes:02d>m
```

Model jest etykietą profilu. Wersja i serial pochodzą z **OTP Inventure**, nie z adresów strony fabrycznej M300. Print time jest zapisanym **czasem drukowania** z NVM ID0, nie całkowitym czasem włączenia. Rekordy są czytane przy każdym otwarciu. Niepewne/brakujące pola osobno pokazują `Unavailable`; prawidłowe zero — `0h 00m`. Otwarcie nie zapisuje pamięci, nie wyświetla kluczy ani surowego OTP/UID.

Release the entry OK button; read the screen; press **OK again** to return. It does not time out after three seconds or require a hold. UP/DOWN do not launch other actions while reading Hardware. The same decoding/formatting logic is used in BOOT and installer.

![Hardware — dane przykładowe](../images/v1.5/08_hardware_example.png)
![Brak wiarygodnych rekordów](../images/v1.5/09_hardware_unavailable.png)

## P4 connection / połączenie

USART6: **PG14 = printer TX → adapter RX**, **PG9 = printer RX ← adapter TX**, common **GND**. **TTL 3.3 V**, no 5 V or RS-232. Do not power the printer from the adapter. Verify actual connector orientation/pin numbering, not a guessed physical order. Use **8N1, no flow control** and the selected saved baud. Only one program may own the port.

```sh
python3 -m pip install pyserial
python3 -m serial.tools.miniterm /dev/cu.YOUR_PORT 250000 --eol LF
```

Use the real port (`/dev/ttyUSB0`, `COM5`, etc.) and baud. Exit miniterm with Ctrl+]. Bootloader echo is on by default; disable local echo. Text commands are uppercase. Stop the five-second autoboot with a button/UART input; after APP starts, `INV>` no longer exists.

### Trwała prędkość / Saved baud

OLED `Diagnostics → UART → P4 baud rate`. Successful selection immediately changes the rate and saves it. `INFO` reports active/saved values. **There is no BAUD text command.** `UP+DOWN` at startup forces 250000 for this boot without overwriting the saved setting. Reinstalling the canonical BOOT resets the journal to 250000; ordinary APP updates preserve it. The journal holds 256 changed-value slots; repeated same selection does not consume another. Interrupted writes may consume a slot; when full, `Settings full` / `LIST_FULL` refuses a new save. No automatic journal erase or wrap.

## Polecenia stałego BOOT / Permanent BOOT commands — INV>

| Polecenie / Command | Działanie / Action |
|---|---|
| HELP | List supported commands |
| INFO | Version, **BUILD RELEASE 1.5-HW2**, mode, limits, board state and active/saved P4 rate |
| PING | PONG <baud> 8N1, DONE OK |
| VERIFY | Verify installed APP without writing |
| LIST | Refresh SD root firmware list; numeric indices from zero |
| SELECT n | Select index from the current list, **not a filename** |
| SELECT AUTO | Reset explicit file selection |
| SDCHECK | Validate selected/automatic SD package; no APP write |
| SDUPDATE | Install APP after physical **OK+UP 2 s** |
| UARTCHECK N | Validate N-byte package supplied by framed IBD1 host protocol |
| UARTUPDATE N | Same with APP installation and physical OK+UP 2 s |
| BOOT | Launch valid APP after **OK+DOWN 2 s** |
| REBOOT | Reset MCU |
| MENU, HOME, BACK | All open main menu; UART BACK is not one-level navigation |
| ECHO ON, ECHO OFF | Enable/disable device UART echo |
| BACKUP | Full Flash + identity to prepared SD files; physical OK+UP 2 s |
| DUMP FLASH/NVM/OTP/UID/OPTIONS | Read-only HEX records with chunk CRC32 and final SHA-256 |
| CARDINFO | SD sector count and capacity |
| DIAG | Button/raw GPIO inputs; no motor/heater actuation |
| DISPLAY | OLED pattern test |
| RESETINFO | Reset flags, boot/watchdog counters and recovery state |
| RECOVERY CLEAR | Clear recovery latch/counter, without automatically launching APP |
| LOG | Last service-history entries |
| LOGSAVE | Save history to prepared SD file; physical OK+UP 2 s |

Most operations report `DONE OK`, or `ERROR <reason>`, followed by READY/INV>. Long tasks may print PHASE/PROGRESS. `DONE ALREADY_INSTALLED` is a skipped identical **APP** write. BOOT/REBOOT do not return to the prior prompt. File selection persists after leaving the browser; `SELECT AUTO` or reset clears it. Automatic candidates: INVENTUR.IVB, InventureUpdate.bin, INVENTUR.BIN. **RESTORE.BIN must be explicitly selected.** Do not paste raw firmware into a text terminal; IBD1 uses READ requests and binary responses with CRC32.

## Instalator to inny program / Installer is a different program — SD>

Menu: **Backup current boot x2; Install / reinstall boot; Hardware; Restart**. Its baud is always **250000 8N1**, not the saved BOOT rate. Its console supports `INFO`, `MEMORY` (four device lines), `BACKUP`, `INSTALL`, `REBOOT`. Use **LF** line endings. Do not send the entire BOOT command set to SD>. INFO retains the r9898/UI-MEM1 family text; the startup banner includes V1.5 HW2. Identify binary bytes by the release manifest.

BOOT replacement requires **two verified current-BOOT backups, valid RESTORE, recognized source, permitted hardware/write conditions and separate physical confirmation**: release, OK once and release, then OK+UP held five seconds. Its four-file SD set is not a general Flash backup toolkit.

## Backup and dumps / Kopie i zrzuty

Permanent BOOT uses preallocated files in FAT32 root: **INVFLASH.BIN 262144 B**, **INVINFO.BIN 1024 B**, and **INVLOG.BIN 4096 B** for history. Fresh templates contain A5 bytes; never overwrite real backups with them. They differ from installer's **ZBACKUP.BIN / ZBACK2.BIN 32768 B each**. An incompatible previous backup is protected by refusal. Backups include current BOOT journal bytes; changing baud can make a previous snapshot differ. Save copies off the SD card and keep device identity private.

| DUMP region | Start | Bytes |
|---|---|---:|
| FLASH | 0x08000000 | 262144 |
| NVM | 0x08008000 | 32768 |
| OTP | 0x1FFF7800 | 528, including locks |
| UID | 0x1FFF7A10 | 12 |
| OPTIONS | 0x1FFFC000 | 16 |

DUMP emits printable `BEGIN_DUMP`, `DATA <offset> <crc32> <hex>` and `END_DUMP SHA256`. Each chunk carries up to 128 actual bytes. A receiver must verify contiguous offsets, length, each CRC32 and final SHA-256; renaming a text log to BIN is not conversion.

History keeps 24 events in CRC-protected backup-SRAM snapshots; retention is for warm resets, not guaranteed power-off persistence. Recovery may latch after three watchdog resets following recorded APP handoffs. This is not detection of every hang and does not enable a new watchdog. Ordinary result screens use their existing timeout; **Hardware is explicitly persistent until a fresh OK press**.

Public host scripts remain [ibtool.py](../../tools/ibtool.py) and [vendor_tool.py](../../tools/vendor_tool.py), without decryption/signing keys. See [APP examples](P4_EXAMPLES.md). No arbitrary-address WRITE, ERASE, RDP-unprotect, tail generator or G-code interface is added.
