# Inventure boot v1.3 — features, OLED menu and UART console

**Author:** Marcin Kowalik · mkowalik@agh.edu.pl. Target: verified Inventure V9, STM32F207 / 256 KiB Flash. Firmware installation and launch have been physically tested by the project owner on both upgrade-from-v1.2 and factory-Zortrax-v1.0 installation paths. The extra v1.3 diagnostics require independent verification on each machine.

## Startup and keys

On power-up the bootloader presents a **3-second countdown**. With a valid installed application and no key/serial interruption, it checks the image and starts the application. Any **UP**, **OK** or **DOWN** button during countdown enters maintenance mode; invalid firmware or latched recovery does the same. An SD image is **never installed automatically** simply because the file is on the card.

**OLED navigation:** UP = previous entry, DOWN = next entry, OK = select. All submenus contain a **Back** item (there is no separate Back key). During destructive operations, the bootloader requests an additional physical confirmation (typically **OK+UP for 2 s** for application installation); booting a stock application requires **OK+DOWN for 2 s**. Follow the actual screen prompts rather than pressing keys speculatively.

### Service menus

| Menu | Actions and effects |
| --- | --- |
| **Start application** | Verify and manually start the installed application; stock firmware may move axes and heat |
| **Firmware on SD** | Scan compatible images, browse/select among up to 16 files in SD root, inspect validity, check, install selected image with confirmation; skip byte-identical firmware |
| **Verify installed** | Read-only integrity verification of the installed app and its firmware metadata |
| **Backup / Recovery** | Export the current 256-KiB main Flash and identity metadata into preallocated SD files, independently verify output, check recovery state; no recovery write is implicit |
| **Diagnostics** | SD reader, buttons, OLED patterns, UART test, read-only GPIO status and reset flags |
| **System information / About** | Boot version, author, contact, app limits, hardware/watchdog checks |
| **Restart / Back** | Controlled software restart or return to previous menu |

Menu labels can vary slightly among builds; rely on the version shown by `INFO`.

## Application update and integrity

- Original encrypted Zortrax `InventureUpdate.bin` using ZRTX AES-CBC container, supported plaintext `INVENTUR.BIN` and custom `.IVB` are recognized only when formats/versions pass verification.
- The bootloader validates the image **before erasing** the application, then writes and reads back; it protects boot sectors 0–1, NVM sectors 2–3, OTP, UID and option bytes.
- A matching application image is **skipped**, without unnecessary erase/program. The source SD update file is intentionally left intact for recovery.
- The application area is `0x08010000` onward. A raw **bootloader** BIN must not be submitted to `SDUPDATE`.

## Backup / SD service files

For v1.3 service operations preallocate on FAT32:
- `INVFLASH.BIN` — **262,144 B** current main Flash;
- `INVINFO.BIN` — **1,024 B** identity / options / integrity metadata;
- `INVLOG.BIN` — **4,096 B** persistent export of the service event log.

These are placeholder files until a backup/export completes successfully; timestamps may not change. Keep copies away from public repositories: Flash/NVM, OTP, UID and device identifiers can contain unique private hardware details. Verify backups and store an independent copy.

## Reset and recovery

`RESETINFO` reports reset-source flags, boot count and recovery latch. After **three watchdog resets following a recorded application handoff**, the autoboot can latch off into recovery; it can be cleared deliberately with `RECOVERY CLEAR`. This logic does **not** treat all power cycles as crashes and does **not** guarantee detection of every frozen application. Hardware watchdog activation is not implicit.

Service history records up to **24 events** with boot identifier and time since boot in backup SRAM, protected by CRC. Its persistence after complete loss of power is not guaranteed; `LOGSAVE` exports the history to prepared SD storage.

## Serial console — access

USART6 is exposed on Inventure **P4 C = PG14/TX**, **P4 D = PG9/RX**, and **P4 G = ground**, 3.3-V logic. On STLINK-V3SET MB1440C, the target-referenced VCP pins connect **CN3 pin 1 (T_VCP_TX) → P4 C**, **CN3 pin 2 (T_VCP_RX) → P4 D**, sharing GND with SWD CN6. Never connect an unverified 5-V USB-TTL TX or supply the board via a TTL VCC lead. The printer has its own properly rated 24-V supply.

Serial settings: **250000 baud, 8N1, no flow control**, LF newline. On macOS (substitute actual device):
```bash
python3 -m serial.tools.miniterm /dev/cu.usbmodem14203 250000 --eol LF
```
Exit with Ctrl+]. Do **not** request terminal local echo if the firmware already echoes keys; the prompt is `INV>`. On application launch the console may stop responding because the original Zortrax firmware takes control.

### Command reference

| Command | Result / effect |
| --- | --- |
| `INFO` | Version, contact/author, current mode, capacity, watchdog and board check |
| `VERIFY` | Verify installed application integrity and identity (read only) |
| `SDCHECK` | Check a recognized update on SD, including crypto/integrity checks (read only) |
| `SDUPDATE` | Request installation of selected/recognized firmware **after on-device physical confirmation**; changes application Flash |
| `BOOT` | Request manual application handoff **after OK+DOWN physical confirmation** |
| `REBOOT` | Software reset |
| `RESETINFO` | Reset reason, boot counts, recovery state |
| `RECOVERY CLEAR` | Deliberately clear recovery latch |
| `PING` | UART/board communication diagnostic |
| `LOG` | Display recent service events |
| `LOGSAVE` | Export log to prepared `INVLOG.BIN` on SD |
| `DUMP FLASH` | Binary transfer of current main Flash via UART with checksums |
| `DUMP NVM` | Export factory NVM range via UART |
| `DUMP OTP` | Export read-only OTP area; treat as sensitive device-specific data |
| `DUMP UID` | Export MCU unique ID; do not post publicly |
| `DUMP OPTIONS` | Export read-only option-byte data |
| `UARTCHECK <length>` | Verify streamed package from a host using the documented framed protocol |
| `UARTUPDATE <length>` | Request streamed package update (physical confirmation still required) |

Some actions are additionally exposed through submenu choices rather than a separate text command. **DUMP uses a binary framed protocol**, not printable terminal text: disconnect miniterm and use the supplied dedicated readback utility. Invalid commands must not result in writes. Never test destructive commands without understanding confirmation and available recovery.

## Validation status and limits

Project owner has confirmed working SD bootloader installation in **both hardware paths** and startup of original Zortrax application. v1.3 offline release tests were recorded as **1099/1099**, but hardware-qualified coverage of new bulk backup, multi-file browsing, UART dumps, and watchdog recovery must be confirmed separately. SD writer uses preallocated files: it does not implement general file creation or a full FAT filesystem manager. A bootloader-sector failure is recoverable via SWD, not necessarily SD.
