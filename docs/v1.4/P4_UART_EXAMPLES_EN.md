# P4 UART console — commands and firmware update examples

> **ARCHIWUM / ARCHIVE v1.4 — P4-PERSIST-r2.** Ten dokument opisuje starsze wydanie, nie bieżącą v1.5. / This document describes the older release, not v1.5.
> [Aktualna dokumentacja / Current docs v1.5](../v1.5/README.md) · [Indeks archiwum / Archive index](README.md)


**Target:** Inventure boot v1.4 `P4-PERSIST-r2`, STM32F207 V9, APP `0x08010000`. [Project](../../README.md) · [Existing complete console reference](FEATURES_AND_CONSOLE_EN.md) · [BOOT installation](INSTALLATION_EN.md) · [Polski](KONSOLA_P4_PRZYKLADY_PL.md)

> The `INV>` prompt exists only while the **custom bootloader** is active. The commands here update **APP only**, not BOOT/NVM/OTP/Option Bytes. This is not stock Zortrax firmware or Klipper G-code console.

## Connect

USART6: printer **PG14 TX → adapter RX**, **PG9 RX ← adapter TX**, common GND. **3.3 V TTL** only; never use RS-232/5 V or power the printer from the USB adapter. Verify physical P4 pin order on the actual board. Interrupt the **5-second** autoboot window to enter maintenance mode. Port setup: **8N1**, no flow control. The saved OLED `Diagnostics → UART → P4 baud rate` rate is 19200, 57600, 115200, 250000, or 500000. Fresh BOOT starts at 250000. Holding **UP+DOWN at power-on/reset** temporarily forces 250000 without erasing the saved choice.

```sh
python3 -m pip install pyserial
python3 -m serial.tools.miniterm /dev/cu.YOUR_PORT 250000 --eol LF
```

Replace the example port and baud as appropriate. Disable local echo (the bootloader echoes); exit with **Ctrl+]** before running an uploader.

## Supported text commands

| Command | Action |
|---|---|
| `HELP`, `INFO`, `PING` | Help, build/state/P4 baud, PONG |
| `VERIFY` | Check installed APP without writing |
| `LIST`, `SELECT n`, `SELECT AUTO` | SD root BIN/IVB file listing (max 16), **zero-based** numeric selection, reset to automatic selection |
| `SDCHECK`, `SDUPDATE` | Validate SD package; install APP after **OK+UP held for 2 s** on printer |
| `UARTCHECK N`, `UARTUPDATE N` | Framed **IBD1** package verification or APP installation (physical OK+UP 2 s) |
| `BOOT`, `REBOOT` | Launch valid APP with **OK+DOWN 2 s**, or reset |
| `MENU`, `HOME`, `BACK` | All open main menu |
| `ECHO ON/OFF` | Serial echo |
| `BACKUP` | Full Flash/identity backup to prepared SD files (physical OK+UP 2 s) |
| `DUMP FLASH/NVM/OTP/UID/OPTIONS` | Read-only printable HEX data with chunk CRC32 and final SHA-256, not a ready BIN |
| `CARDINFO`, `DIAG`, `DISPLAY` | Card information, button/GPIO input, OLED patterns |
| `RESETINFO`, `RECOVERY CLEAR`, `LOG`, `LOGSAVE` | Recovery state and service history |

Success typically prints `DONE OK`; failure `ERROR <reason>`; long tasks include `PHASE`/`PROGRESS`. `DONE ALREADY_INSTALLED` means identical image skipped. There is **no** `BAUD`, `SELECT <filename>`, `ERASE`, `WRITE 0x...`, or `M997` command.

## Back up before any update

Use FAT32 with preallocated `0xA5`-filled **INVFLASH.BIN (262144 bytes)** and **INVINFO.BIN (1024 bytes)**; `INVLOG.BIN (4096 bytes)` is used for `LOGSAVE`. Never replace real backups with templates. After `BACKUP` and physical OK+UP 2 s, save verified backups to separate media. Keep UID/NVM/OTP private. `DUMP FLASH` is ASCII text `BEGIN_DUMP / DATA offset crc32 HEX / END_DUMP SHA256`; a `.txt` rename to `.bin` does not decode it.

## Example A — original encrypted Zortrax `InventureUpdate.bin`

The vendor path accepts only **eight exact known stock application images** after validation (ZRTXUINV, vectors, HMAC, SHA-256); a version label is insufficient. Put the supported encrypted `InventureUpdate.bin` in FAT32 root with no competing packages. At `INV>`:

```text
LIST
SELECT 0
SDCHECK
SDUPDATE
VERIFY
BOOT
```

**Use the actual zero-based index from `LIST`**: 0 is illustrative. `SDUPDATE` needs OK+UP 2 s on the panel. After successful `VERIFY`, `BOOT` requires OK+DOWN 2 s. APP is changed; BOOT and factory NVM are preserved.

**Encrypted ZRTX over UART:** the public [`tools/vendor_tool.py`](../../tools/vendor_tool.py) contains **no AES key** and cannot decrypt `InventureUpdate.bin`. The public `ibtool.py serial` sender expects a valid **IVB**, not encrypted ZRTX. Use the **SD route above** for a supported encrypted vendor file — the bootloader itself recognizes and validates it.

You may inspect the outer ZRTX envelope **without decrypting any application bytes**:

```sh
python3 tools/vendor_tool.py InventureUpdate.bin
# Reports outer revision/size only.
# --ivb-out with encrypted input is explicitly rejected.
```

For actual UART transfer of a stock application, supply an **already decoded** known APP and follow Example B. No AES key, vendor HMAC key, `tail20` contents or tail-generating routine are published.

## Example B — decoded original stock APP

A known decoded stock application has vectors for `0x08010000`, internal magic `0x12345678` at offset `0x1C`, size at `0x20`, revision `rNNNN` at `0x24`, and may have HMAC plus `0xCD` padding. The exact eight-image stock allowlist still applies. **A 262144-byte full Flash dump is not APP.**

For supported `application_r0323.bin` or verified `RESTORE.BIN` on FAT32 SD root:

```text
LIST
SELECT 1
SDCHECK
SDUPDATE
VERIFY
BOOT
```

1 is only an example; read the real index. `RESTORE.BIN` must be selected explicitly.

For UART, the **public** [`tools/vendor_tool.py`](../../tools/vendor_tool.py) packages an **already decoded** known stock APP after comparing its SHA-256 with eight archived references. The **public** [`tools/ibtool.py`](../../tools/ibtool.py) inspects and transfers IVB, without decrypting vendor firmware or producing a vendor tail:

```sh
python3 -m pip install pyserial
python3 tools/vendor_tool.py application_r0323.bin --ivb-out STOCK_RAW_R0323.IVB
python3 tools/ibtool.py inspect STOCK_RAW_R0323.IVB
# Check only: UARTCHECK, no Flash write
python3 tools/ibtool.py serial STOCK_RAW_R0323.IVB --port /dev/cu.YOUR_PORT --baud 250000
# Then explicit write: UARTUPDATE with OK+UP 2 s on the printer
python3 tools/ibtool.py serial STOCK_RAW_R0323.IVB --port /dev/cu.YOUR_PORT --baud 250000 --update
```

**Important distinction:** an input containing *only the raw stock APP body* produces a **custom-manifest IVB with the same APP code**, but **not a byte-identical manufacturer payload** — no vendor tail is synthesized. An **already existing complete** plaintext vendor payload (with its tail/padding) is preserved only if its **full SHA-256** matches a known reference. No secret signing key is used. This custom-manifest raw-stock route is not a separately confirmed physical hardware test. For canonical original firmware, prefer the verified `RESTORE.BIN` or supported encrypted ZRTX via SD. Never feed a full Flash dump as APP.

## Example C — custom APP, e.g. Klipper

You need a real **STM32F207 V9** application compiled/linked at **0x08010000**, with correct clocks, GPIO, peripherals, thermal safety and host settings. A generic `klipper.bin` is **not compatible by name**. The custom unencrypted `INVB001` format uses a 64-byte header, target `0x32463956`, base `0x08010000`, length and SHA-256. Raw APP payload is **8–196352 bytes**, with valid aligned MSP in 128 KiB SRAM and Thumb Reset vector within the payload. These structural conditions **do not prove safe operation**.

Use the **public** [`tools/ibtool.py`](../../tools/ibtool.py) to package and check a V9-specific raw app:

```sh
python3 tools/ibtool.py pack klipper.bin KLIPPER_V9.IVB
python3 tools/ibtool.py inspect KLIPPER_V9.IVB
```

For **SD**, copy `KLIPPER_V9.IVB` to root then use `LIST → SELECT n → SDCHECK → SDUPDATE → VERIFY → BOOT`, with the same physical confirmations. A custom validated APP may display `CUSTOM_MANIFEST` after `VERIFY`.

For **P4 file upload** from a host computer:

```sh
python3 tools/ibtool.py serial KLIPPER_V9.IVB --port /dev/cu.YOUR_PORT --baud 250000
python3 tools/ibtool.py serial KLIPPER_V9.IVB --port /dev/cu.YOUR_PORT --baud 250000 --update
```

The uploader replies to `READ <offset> <count>` with binary **IBD1 frames and CRC32**. Pasting a raw BIN into miniterm or just typing `UARTUPDATE N` will not transfer it. Once Klipper APP runs, `INV>` disappears and Klippy uses its own serial protocol. Existing Klipper port work has software checks, **not a complete physical safety acceptance of heaters, motion, sensors and interlocks**.

**Rollback:** interrupt the next bootloader countdown and re-install a verified stock APP through SD/UART; require `VERIFY` then `BOOT`. No automatic A/B rollback.

## Errors

`NOTFOUND`/`AMBIGUOUS_FILES`: adjust file selection. `FORMAT`/`RANGE`/`VECTOR`: wrong image/target/vectors. `HASH`/`CRC`/`CHANGED`: integrity/transfer issue. `VENDOR_UNKNOWN_IMAGE`: vendor image not in the allowlist. `CONFIRM`/`BUTTONS`: physical confirmation missing. `HARDWARE`/`FLASH`/`READONLY`: write prerequisites not met. `NO_COMMIT`/`HW_WATCHDOG`: invalid APP metadata or recovery condition. Never bypass refusals by changing protection, erasing NVM or overwriting BOOT.
