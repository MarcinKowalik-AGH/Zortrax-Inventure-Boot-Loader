# P4 — application update examples / przykłady aktualizacji APP

[Project](../../README.md) · [Console reference](FUNKCJE_I_KONSOLA.md) · [BOOT installation PL](INSTALACJA_PL.md) · [BOOT installation EN](INSTALLATION_EN.md)

These examples operate in **permanent BOOT INV>**, not the temporary SD> installer and not the running printer APP. They replace **APP from 0x08010000**, not BOOT. They do not change NVM/OTP/protection. Use a verified device backup and a suitable image. Numerical indices and serial-port names below are placeholders/examples, not measurements from a live session.

**Hardware — potwierdzone na urządzeniu:** 29.10.2026 właściciel dodatkowo potwierdził, że ekran Hardware w stałym bootloaderze **poprawnie odczytuje rzeczywiste dane jego drukarki**. Nie jest to jedynie wynik testu modelowego. Ilustracje w instrukcji nadal zawierają jawnie syntetyczne dane przykładowe; nie są zrzutem prywatnych danych użytkownika.

**Hardware — physically confirmed:** on 29 October 2026 the owner explicitly confirmed that the permanent bootloader Hardware screen **correctly reads the actual printer data** on his device. This is an on-device confirmation, not just a model test. Manual previews still use clearly synthetic examples rather than private printer data.

## 1. Original encrypted Zortrax package — SD

Place a supported authentic `InventureUpdate.bin` in FAT32 root. Interrupt BOOT autoboot. Send commands one at a time, checking each result:

```text
LIST
SELECT 0
SDCHECK
SDUPDATE
VERIFY
BOOT
```

**Use the actual index from LIST**, not necessarily 0. SDCHECK must succeed first. SDUPDATE requires **release → OK+UP 2 s**; BOOT requires **release → OK+DOWN 2 s**. Only recognized vendor images pass the vendor path; a filename/version label alone is insufficient. Public `vendor_tool.py` **does not decrypt ZRTX**. Its optional inspection of an encrypted file reports only outer metadata; `--ivb-out` is deliberately refused for encrypted input. Install encrypted stock through SD.

## 2. Already decoded original APP — SD or P4

Use a known `application_r0323.bin`, or supplied verified **RESTORE.BIN** explicitly selected by `LIST` / `SELECT n`. A full 256-KiB Flash dump is not an APP. Do not strip a complete original tail/padding just to make a file pass. For host-side UART preparation, run from the repository root:

```sh
python3 -m pip install pyserial
python3 tools/vendor_tool.py application_r0323.bin --ivb-out STOCK_RAW_R0323.IVB
python3 tools/ibtool.py inspect STOCK_RAW_R0323.IVB
python3 tools/ibtool.py serial STOCK_RAW_R0323.IVB --port /dev/cu.YOUR_PORT --baud 250000
# Only after check-only succeeds, and with physical OK+UP 2 s when requested:
python3 tools/ibtool.py serial STOCK_RAW_R0323.IVB --port /dev/cu.YOUR_PORT --baud 250000 --update
```

Both [vendor_tool.py](../../tools/vendor_tool.py) and [ibtool.py](../../tools/ibtool.py) are public. Close the interactive terminal before using the sender. Replace port/baud with the actual active BOOT settings. The first `serial` performs UARTCHECK; `--update` performs UARTUPDATE and still needs physical confirmation. After completion reopen the console, run VERIFY, then BOOT with its separate confirmation.

A raw decoded APP body wrapped in IVB becomes a **custom-manifest representation of that code**, not an exact reconstruction of the manufacturer's full payload. No vendor tail20 is generated. A complete existing plaintext stock payload is preserved only when its full digest matches a known reference. For canonical stock restoration prefer the supplied RESTORE.BIN or supported encrypted ZRTX via SD. These alternatives are not separately claimed as hardware-tested by the one-printer HW2 report.

## 3. Custom APP — e.g. Klipper for Inventure V9

Use a genuine V9-specific **STM32F207** raw application linked at **0x08010000**, with appropriate clock/pins/USART6 and safety behavior. A generic klipper.bin for another board is not compatible by name. Payload must fit **8–196352 bytes**, have a valid 8-byte-aligned MSP in 128 KiB SRAM, and a Thumb reset vector inside the APP payload. An ELF, whole Flash dump or BOOT image is not the input.

```sh
python3 tools/ibtool.py pack klipper.bin KLIPPER_V9.IVB
python3 tools/ibtool.py inspect KLIPPER_V9.IVB
python3 tools/ibtool.py serial KLIPPER_V9.IVB --port /dev/cu.YOUR_PORT --baud 250000
python3 tools/ibtool.py serial KLIPPER_V9.IVB --port /dev/cu.YOUR_PORT --baud 250000 --update
```

Alternatively copy KLIPPER_V9.IVB to SD root and use LIST → actual SELECT n → SDCHECK → SDUPDATE → VERIFY → BOOT. IVB uses a 64-byte INVB001 header and SHA-256; this is **integrity metadata, not a manufacturer signature or proof of safe heater/motion behavior**. Do not patch vectors by hand to bypass a validation error.

The host responds to READ requests with binary **IBD1** frames and CRC32. `cat firmware.bin` into a terminal is not this protocol. After BOOT transfers control to Klipper MCU, INV> disappears and Klippy uses its own protocol/settings. A successful bootloader update does not certify a Klipper port.

To restore stock, stop autoboot at the next reset and install a verified original APP; require VERIFY before BOOT. There is no automatic A/B rollback. This does not install a new permanent bootloader; for that use the three documented BOOT packages.

## Po polsku — kluczowe rozróżnienia

Polecenia w blokach `sh` wpisuje się **na komputerze**, nie po INV>. W konsoli BOOT wybór pliku jest numerem z aktualnego LIST; nie ma `SELECT RESTORE.BIN`. Publiczne skrypty nie odszyfrowują ZRTX i nie odtwarzają tail20. Sam poprawny pakiet IVB oznacza zgodność struktury i sum, nie kompletne sprawdzenie alternatywnego firmware na drukarce. Po zapisie sprawdź VERIFY, a dopiero potem potwierdź BOOT. Prędkość konsoli i prędkość uruchomionej APP mogą być różne.
