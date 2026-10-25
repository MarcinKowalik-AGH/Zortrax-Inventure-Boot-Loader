# P4 UART console — commands and firmware update examples

**Target:** Inventure boot v1.4 `P4-PERSIST-r2`, STM32F207 V9, APP `0x08010000`. [Project](../README.md) · [Existing complete console reference](FEATURES_AND_CONSOLE_EN.md) · [BOOT installation](INSTALLATION_EN.md) · [Polski](KONSOLA_P4_PRZYKLADY_PL.md)

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

For an actual file transfer **over UART**, the private `vendor_tool.py` converts a verified known vendor ZRTX into IVB; the `ibtool.py serial` host accepts **IVB only**, not raw ZRTX:

```sh
python3 tools/vendor_tool.py InventureUpdate.bin --ivb-out STOCK_R0323.IVB
python3 tools/ibtool.py inspect STOCK_R0323.IVB
python3 tools/ibtool.py serial STOCK_R0323.IVB --port /dev/cu.YOUR_PORT --baud 250000
python3 tools/ibtool.py serial STOCK_R0323.IVB --port /dev/cu.YOUR_PORT --baud 250000 --update
```

These commands run on the **host computer**, not at `INV>`. The first serial call uses read-only `UARTCHECK`; the `--update` call uses `UARTUPDATE`, still with physical confirmation. They require the **private full source/tool package**, not included among the three publicly published firmware binaries. Encrypted vendor conversion needs OpenSSL; serial needs pySerial. Close miniterm first.

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

1 is only an example; read the real index. `RESTORE.BIN` must be selected explicitly. For UART, create IVB using the same private known-image tool:

```sh
python3 tools/vendor_tool.py application_r0323.bin --ivb-out STOCK_RAW_R0323.IVB
python3 tools/ibtool.py inspect STOCK_RAW_R0323.IVB
python3 tools/ibtool.py serial STOCK_RAW_R0323.IVB --port /dev/cu.YOUR_PORT --baud 250000 --update
```

Do not strip vendor tails/padding speculatively and do not transmit full Flash dumps as APP.

## Example C — custom APP, e.g. Klipper

You need a real **STM32F207 V9** application compiled/linked at **0x08010000**, with correct clocks, GPIO, peripherals, thermal safety and host settings. A generic `klipper.bin` is **not compatible by name**. The custom unencrypted `INVB001` format uses a 64-byte header, target `0x32463956`, base `0x08010000`, length and SHA-256. Raw APP payload is **8–196352 bytes**, with valid aligned MSP in 128 KiB SRAM and Thumb Reset vector within the payload. These structural conditions **do not prove safe operation**.

Use the **private** `tools/ibtool.py` to package and check a V9-specific raw app:

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
