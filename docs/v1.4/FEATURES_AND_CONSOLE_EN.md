# Inventure boot v1.4 — OLED menu, features and UART console

> **ARCHIWUM / ARCHIVE v1.4 — P4-PERSIST-r2.** Ten dokument opisuje starsze wydanie, nie bieżącą v1.5. / This document describes the older release, not v1.5.
> [Aktualna dokumentacja / Current docs v1.5](../v1.5/README.md) · [Indeks archiwum / Archive index](README.md)


**Release:** `P4-PERSIST-r2` · **Author:** Marcin Kowalik · mkowalik@agh.edu.pl  
**Target:** a recognized Inventure V9 with STM32F207 and 256 KiB Flash. File identities are listed in the [release manifest](RELEASE_MANIFEST.md). Flashing procedures are in the [installation guide](INSTALLATION_EN.md). [Polski](FUNKCJE_I_KONSOLA_PL.md).

The owner has confirmed uploading this corrected build to the printer and successfully testing its options. This records operation on that device; it does not stand in for separate electrical measurements or testing every failure scenario.

## Startup, buttons and result screens

A **5-second countdown** starts after display initialization. The bootloader checks the application in Flash and launches it when the startup conditions are satisfied. Any panel button — **UP, OK or DOWN** — cancels the countdown and opens the menu. A press during initialization is also recognized. A received UART character cancels autoboot as well. An invalid application, incompatible hardware conditions or a recovery latch prevents automatic launch.

An image is **not installed merely because it is present on SD** in this bootloader. Automatic startup refers to the application already stored in the printer.

UP and DOWN move the selection; OK opens or runs the selected item. `Back` is the first submenu entry and stays visible in the top row while the other entries scroll. Its selected marker points **left**; markers for other entries point right. The selected-file page uses `Back to files`. There is no separate Back button.

An ordinary result screen, such as `OPERATION COMPLETE` / `OK` or `OPERATION REJECTED` / an error code, returns to the menu **automatically after 3 seconds**. Button presses do not trigger another action while it is visible. Release the buttons, wait for the menu, then make a fresh press. Do not press OK to dismiss a result.

| Operation | Physical confirmation | Cancel |
| --- | --- | --- |
| Write an application from SD or UART | Release all buttons, then hold **OK + UP for 2 s** | DOWN alone |
| Manually launch the application | Release all buttons, then hold **OK + DOWN for 2 s** | UP alone |
| `Backup Flash + identity` / `BACKUP` and `Save history to SD` / `LOGSAVE` | Release all buttons, then **OK + UP for 2 s**; these operations write SD files | DOWN alone |

Confirmation first displays `RELEASE BUTTONS`, followed by the required combination. A valid automatic launch after the countdown does not require the manual-launch combination. The separate r9898 BOOT installer has its own menu and two BOOT-replacement confirmations, including a 5-second hold; see the installation guide.

## Complete r2 menu

The following labels and order are exact for `P4-PERSIST-r2`. Screens use English labels, the heading `Inventure boot v1.4 © Marcin Kowalik`, and the proportional bitmap font recovered from the original Zortrax r0323 application. Its pixels and spacing are retained, with this bootloader's own heading and four visible menu rows. This does not claim identical appearance to every historical factory bootloader screen.

| Main-menu entry, in order | Submenu entries, in order |
| --- | --- |
| `Start application` | `Back`, `Launch application` |
| `Firmware on SD` | `Back`, `Check SD package`, `Install firmware`, `Choose firmware file` |
| `Diagnostics` | `Back`, `Verify Flash`, `Hardware status`, `Reset / Recovery`, `Clear recovery lock`, `Buttons / raw inputs`, `Display test`, `UART`, `SD card info` |
| `About` | `Back`, `© Marcin Kowalik`, `mkowalik@agh.edu.pl`, `Version v1.4` |
| `Restart` | `Back`, `Restart controller` |
| `Backup Flash` | Page title `Backup to SD`: `Back`, `Backup Flash + identity` |
| `Service history` | `Back`, `View history on UART`, `Save history to SD` |

| Further page | Entries, in order |
| --- | --- |
| `Diagnostics → UART` | `Back`, **`UART test`**, **`P4 baud rate`** |
| `Diagnostics → UART → P4 baud rate` | `Back`, `19200`, `57600`, `115200`, `250000`, `500000` |
| `Firmware on SD → Choose firmware file` | Title `Files - select, then verify`; `Back`, followed by the discovered files |
| Selected file | The filename is the title; `Back to files`, `Check selected file`, `Install selected file` |

`UART` is immediately **after `Display test` and before `SD card info`**. The two UART functions are inside that submenu. Installed-application verification is `Diagnostics → Verify Flash`; launch is `Start application → Launch application`. `VERIFY` and `BOOT` below are console command names.

## Firmware files and application installation

The browser lists up to **16 `.BIN` / `.IVB` files** in the SD root directory, within the supported name and size limits. It supports FAT short names and valid ASCII VFAT names up to 26 characters. It does not recurse into folders or open ZIP archives. Reserved backup and log filenames are excluded from firmware browsing. FAT16/FAT32 cards are supported; use FAT32 for the installation procedures. exFAT is not supported.

**Selecting a file does not verify it.** Run `Check selected file`, wait for success, and separately choose `Install selected file`. Checks cover structure, vectors and integrity; supported original images also undergo the relevant container and known-image checks. A BIN extension alone does not make a file compatible firmware.

Recognized formats include compatible `.IVB` packages, supported Zortrax plaintext payloads and original encrypted ZRTX `InventureUpdate.bin` packages. Verification precedes application erase, and readback verifies the written result. An image already identical to the installed application produces `ALREADY INSTALLED` / `FLASH WRITE SKIPPED` on OLED and `DONE ALREADY_INSTALLED` on UART.

Without an explicit selection, `Check SD package` / `SDCHECK` and `Install firmware` / `SDUPDATE` use the standard names `INVENTUR.IVB`, `InventureUpdate.bin`, `INVENTUR.BIN`. Leaving multiple candidates can produce `AMBIGUOUS_FILES`. **Select `RESTORE.BIN` explicitly in the browser**; it is not one of the automatic-selection names.

The selected file remains selected after leaving through `Back`; subsequent general `SDCHECK` / `SDUPDATE` commands still use it. A restart or `SELECT AUTO` restores automatic selection. After a successful install, the bootloader returns to the menu; manual launch is a separate action.

`SDUPDATE` and `UARTUPDATE` write the **application area starting at `0x08010000`**, including its metadata. They do not directly install a raw 32-KiB BOOT image. An ordinary application update leaves BOOT, its P4 journal, NVM, OTP and option bytes outside the write operation. BOOT replacement has a separate procedure. Interrupted programming may require application recovery or SWD intervention; there is no automatic rollback to a second image.

## P4 baud rate — persistent settings

**`Diagnostics → UART → P4 baud rate`** offers **19200, 57600, 115200, 250000 and 500000 baud**. A freshly programmed canonical BOOT image defaults to **250000**. The remaining serial settings are **8N1, no flow control**.

1. Select a rate on the panel and press OK. After a successful save, the rate changes immediately; there is no additional 2-second confirmation.
2. Change the terminal to the same rate. The `PONG <rate> 8N1` and `P4 SAVED` responses already use the new rate.
3. Send `PING`. At 115200, for example, the response is `PONG 115200 8N1`, followed by `DONE OK`.
4. On the next reset or power-on, the saved rate is restored before the first `INFO` output. No SD card is needed.

The rate is selected through the OLED menu; there is no text `BAUD` command. Do not change it halfway through entering a command or during a transfer. A partial console line or busy operation blocks a rate change with `BUSY`.

In `INFO`, `P4_BAUD 115200 8N1 SAVED 115200` reports the active and saved rates. They can differ during the recovery startup described below.

### If you have forgotten the saved rate

Hold **UP + DOWN during power-on or reset**, until you enter the menu. This startup uses **250000 baud** while retaining the saved value. Connect at 250000 and check `INFO`. The previously saved rate returns on the next ordinary restart. To save 250000 permanently, deliberately select it in `P4 baud rate`.

### Journal capacity and BOOT reinstallation

The setting journal occupies the last **256 bytes of BOOT**, `0x08007F00–0x08007FFF`. It has **256 slots for changed saved selections**. Selecting the value already saved consumes no new slot. An interrupted attempt can consume a slot without producing a valid record, so 256 slots do not guarantee 256 successful changes under all conditions.

A normal rate change appends a record without erasing a sector. Once the journal is full, a new selection is rejected: OLED shows `P4 not saved` / `Settings full`, and UART reports `ERROR LIST_FULL`. The active and last valid saved settings are retained. There is no automatic wraparound or journal erase.

**Reinstalling the canonical BOOT image through r9898 or ST-Link resets the journal and restores 250000.** This also applies to an r1 → r2 upgrade. An ordinary application update does not erase it. Raw full 32-KiB BOOT backups include the previous P4 settings. Saving a rate does not modify factory NVM, OTP or option bytes.

This setting belongs to the bootloader console. The r9898 installer always initializes its own **250000 8N1** connection; Zortrax and Klipper applications have their own port configuration. The `INV>` prompt stops operating once control is handed to an application.

## Connecting the console

The bootloader uses **USART6**, with **PG14 = printer TX** and **PG9 = printer RX**, exposed through the project's P4 console connection. Connect according to signal function:

| Printer signal | UART adapter connection |
| --- | --- |
| Printer TX, PG14 | Adapter RX |
| Printer RX, PG9 | Adapter TX |
| GND | Common ground |

Use **3.3-V logic**. This table does not specify physical pin order, connector viewing direction or the numbering of a particular adapter. Establish those from the documentation or a verified connection for that board and adapter. Do not connect a 5-V transmitter or RS-232 voltage levels. Do not power the board from the UART adapter's VCC lead; the printer uses its own supply.

Set the terminal to the active rate, **8N1, no flow control**. LF is a suitable line ending; r2 also accepts CR and CRLF. Commands are uppercase. The prompt is `INV>`. Bootloader echo is on by default, so enabling terminal local echo as well produces doubled characters. Use `ECHO OFF` / `ECHO ON` to control bootloader echo.

Example for macOS with pySerial installed — replace the port name and use the rate selected on the panel:

```sh
python3 -m serial.tools.miniterm /dev/cu.YOUR_PORT 250000 --eol LF
```

Terminal reference: [pySerial miniterm](https://pyserial.readthedocs.io/en/latest/tools.html#serial-tools-miniterm). Exit miniterm with **Ctrl+]**. Only one program should use the port at a time. Switch to 250000 after launching the installer; after launching the user application, do not expect the BOOT console to respond.

**[Practical P4 UART examples: encrypted stock, decoded stock and Klipper](P4_UART_EXAMPLES_EN.md)** — SD and framed UART update walkthroughs.

## UART commands and responses

Ordinary success is reported as `DONE OK`; errors use `ERROR <code>`. Most commands finish with `READY` and the `INV>` prompt. Successful `BOOT` and `REBOOT` hand off control or reset the device, so they do not finish at the old prompt. Longer operations also produce `PHASE` and `PROGRESS` lines.

| Command | Action / characteristic response |
| --- | --- |
| `HELP` | Command list; `DONE OK` |
| `INFO` | Version, `BUILD P4-PERSIST-r2`, mode, APP limits, hardware status and `P4_BAUD … 8N1 SAVED …` |
| `VERIFY` | Verify the APP in Flash; success prints `INSTALLED <byte_count> <name_or_CUSTOM_MANIFEST>`, then `DONE OK` |
| `LIST` | Refresh the file list: `FILES <count> (NOT YET VERIFIED)`, followed by each index, name and size |
| `SELECT n` | Select a **zero-based** index from the last list; `SELECTED <name>`, `DONE OK` |
| `SELECT AUTO` | Clear the explicit selection; `DONE AUTO_SELECTION` |
| `SDCHECK` | Check the selected or automatically discovered package without writing APP |
| `SDUPDATE` | Install the verified package after physical OK+UP for 2 s; an identical image returns `DONE ALREADY_INSTALLED` |
| `BOOT` | Launch a valid APP after OK+DOWN for 2 s; handoff prints `BOOT APPLICATION` |
| `REBOOT` | Restart the device |
| `MENU`, `HOME`, `BACK` | All three open the **main menu**; UART `BACK` does not navigate up just one page |
| `ECHO ON`, `ECHO OFF` | Respectively `DONE ECHO_ON`, `DONE ECHO_OFF` |
| `BACKUP` | Save Flash and identity to SD; successful verification prints `BACKUP VERIFIED: INVFLASH.BIN + INVINFO.BIN`, then `DONE OK` |
| `RESETINFO` | Reset flags/cause, `BOOT_COUNT`, `WDG_LOOP_COUNT`, `RECOVERY OFF` or `LATCHED`, `RETENTION WARM_RESET_ONLY` |
| `RECOVERY CLEAR` | Clear the recovery counter/latch; `RECOVERY CLEARED`, `DONE OK`; does not launch APP |
| `DIAG` | Button test, followed by `RAW_IDR` reads of ports A/C/D/G |
| `DISPLAY` | Display-pattern test |
| `PING` | `PONG <active_rate> 8N1`, `DONE OK` |
| `CARDINFO` | SD initialization, sector count `SD_SECTORS` and capacity `SD_MiB` |
| `LOG` | `HISTORY LAST … OF … EVENTS`, followed by `EVENT` lines |
| `LOGSAVE` | Save history to prepared `INVLOG.BIN`, after panel confirmation |
| `DUMP FLASH`, `DUMP NVM`, `DUMP OTP`, `DUMP UID`, `DUMP OPTIONS` | Read memory in the text HEX format described below |
| `UARTCHECK N` | Check an N-byte package supplied by a host using the framed protocol |
| `UARTUPDATE N` | Install such a package; physical write confirmation is still required |

To select a file, run `LIST`, read its current index, then send, for example, `SELECT 1`. File order depends on the card directory. **There is no `SELECT RESTORE.BIN` or `SELECT <filename>` command.** `SELECT` does not verify a package; use `SDCHECK` for that.

`UARTCHECK` / `UARTUPDATE` are intended for a host program. The bootloader requests chunks with `READ <offset> <byte_count>`, and the host responds with an `IBD1` frame containing offset, length, data and CRC32. Do not send a raw firmware file as terminal text. This input protocol is separate from the text `DUMP` export.

## DUMP — text HEX with integrity checks

`DUMP` is read-only. It returns **printable ASCII text with hex-encoded data**, not a ready-to-use binary file. Its structure is shown below; angle-bracket fields stand for actual values returned by the device:

```text
BEGIN_DUMP FLASH 262144
DATA <offset_hex8> <crc32_hex8> <hex_data>
...
END_DUMP SHA256 <sha256_hex64>
DONE OK
READY
INV>
```

Each `DATA` line contains up to **128 data bytes**, represented by up to 256 HEX characters. The offset is relative to the start of the selected region; CRC32 covers that chunk's bytes. The final SHA-256 covers all bytes in the region. A large export, particularly full Flash at 19200 baud, needs enough time to transmit the complete text stream.

| Command | Region start | Byte count |
| --- | --- | ---: |
| `DUMP FLASH` | `0x08000000` | 262144 |
| `DUMP NVM` | `0x08008000` | 32768 |
| `DUMP OTP` | `0x1FFF7800` | 528, including lock bytes |
| `DUMP UID` | `0x1FFF7A10` | 12 |
| `DUMP OPTIONS` | `0x1FFFC000` | 16 |

The complete stream can be saved as a text log. To produce a valid `.bin`, a receiver must decode only the data fields and verify contiguous offsets, total length, each chunk's CRC32 and the final SHA-256. Renaming the log to `.bin` does not perform that conversion. Do not treat an interrupted, unchecked stream as a valid backup. Flash/NVM, OTP and UID dumps may contain details unique to the printer; keep them private.

## Backup Flash and SD service files

`Backup Flash → Backup Flash + identity` or `BACKUP` saves the **current state** of the 256-KiB main Flash, including BOOT, its P4 journal, NVM and APP. It is not necessarily a factory snapshot. Identity data and checksums accompany it. Prepare these files in the FAT32 root directory before use:

| File | Exact size | Contents after success |
| --- | ---: | --- |
| `INVFLASH.BIN` | 262144 B | Entire current main Flash |
| `INVINFO.BIN` | 1024 B | UID, OTP with locks, option-byte readout, Flash SHA-256 and metadata integrity fields |
| `INVLOG.BIN` | 4096 B | Service-history export through `LOGSAVE` |

Fresh templates must contain **`0xA5` bytes** throughout and have the exact sizes above. Their presence does not mean a backup has been made. The bootloader writes already allocated file extents; it does not create, resize, rename or update file timestamps. A missing required service file produces `PREPARE_SD_FILES`.

Backup accepts A5 sectors or sectors already matching the current device contents. A different earlier backup is protected from replacement and produces `BACKUP_EXISTS`. Save that backup on a computer before preparing fresh templates. A P4 rate change alters BOOT bytes, so an earlier backup may no longer match current memory. Writing is followed by readback and SHA-256 verification, with metadata written last.

`INVLOG.BIN` can be replaced by another log from the same device. It is not an unlimited journal. Copy successful backups/exports to independent storage as well. `INVINFO.BIN` is a metadata file, not an image to program into the MCU.

These files are separate from the **32768-byte `ZBACKUP.BIN` and `ZBACK2.BIN`** used by r9898 during BOOT replacement. Do not interchange their names or purposes.

## Diagnostics, history and recovery

`Buttons / raw inputs` / `DIAG` shows button states and reads GPIO inputs. **Hold OK alone for 1 s** to finish; the test also has a 20-second timeout. `Display test` / `DISPLAY` shows OLED patterns: **UP/DOWN changes the pattern, OK exits**, also with a 20-second timeout. `UART test` displays the active rate and `Send PING`; UART prints `PONG … 8N1`. `SD card info` initializes the card and reports capacity. These functions are not motion, heating, thermistor-calibration or power-stage tests.

`Reset / Recovery` / `RESETINFO` reports reset flags, boot count, watchdog-reset count and the recovery latch. **Three watchdog resets following recorded APP handoffs** can block autoboot. `Clear recovery lock` / `RECOVERY CLEAR` deliberately clears this counter/latch without launching the application. Manual launch of a valid APP still requires the normal confirmation. Power loss, BOR, NRST and intentional software reset are not treated as confirmed failed launches. The mechanism does not detect every hang and does not enable a new watchdog.

History retains the last **24 events**, boot sequence number and milliseconds since that boot. It uses two CRC-protected state snapshots in backup SRAM. Retention is expected across warm resets; it is not guaranteed after complete power loss. `LOG` prints the history, and `LOGSAVE` saves its current snapshot to SD. It is not a dated wall-clock log or a full crash dump.

## Useful refusal messages

| Message | Practical meaning |
| --- | --- |
| `NOTFOUND` | The required firmware file was not found |
| `AMBIGUOUS_FILES` | File selection is ambiguous; remove spare candidates or explicitly select the intended file |
| `HASH`, `CRC`, `VECTOR`, `FORMAT` | A data, image or protocol check failed; do not force a write |
| `CONFIRM`, `BUTTONS` | Confirmation was cancelled/incomplete, or buttons were not released |
| `HARDWARE` | A combined hardware/write-condition refusal; the code alone does not identify a single cause |
| `HW_WATCHDOG` | Watchdog conditions block APP handoff |
| `BACKUP_EXISTS` | An existing backup differs from the current device/image; preserve it before preparing a new one |
| `PREPARE_SD_FILES` | A prepared service file is missing, or the log template is incompatible |
| `LIST_FULL` | In browsing: too many files; during a P4 change: a full journal, with `Settings full` on OLED |
| `BUSY` | The P4 rate cannot be changed now, for example while a UART line is incomplete |

When investigating a problem, retain the exact message, the action that produced it and the `INFO` output. These commands do not change MCU protection settings.
