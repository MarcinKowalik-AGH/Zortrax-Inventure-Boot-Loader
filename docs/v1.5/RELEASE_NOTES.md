# Inventure boot v1.5 — RELEASE 1.5-HW2

Wydanie / Release 29.10.2026. Zortrax Inventure V9 / STM32F207 / 256 KiB.

**Owner report:** installed on one printer; everything works. These are the exact HW2 files supplied before that report, with no recompilation or binary patching. The pre-test installer banner HW UNTESTED remains and is explained in the manuals. One printer is not separate acceptance of all routes or failure modes.

**Changes:** original unscaled r0323 font in BOOT and installer; read-only Hardware with actual OTP/NVM fields; non-wrapping stateful menus and correct Back detection; partial OLED transfers; lossless text storage optimization. Boot/NVM/APP addresses and P4 persistence remain unchanged.

**Three distributions:** SD_UPGRADE for recognized custom BOOT; SD_FACTORY_V9 (FROM FACTORY) for exact compatible original BOOT with required write conditions; standalone STLINK 32-KiB BIN at 0x08000000. Download the SHA256SUMS file and verify before installation.

**SD routes must restore APP afterwards using the supplied RESTORE.BIN** (stock 1.6.1/r0323). BOOT replacement resets P4 to 250000 8N1. ST-Link writes sectors 0–1 only. No Mass Erase, read-unprotect or option-byte changes to bypass refusals.

v1.4 artifacts and manuals remain available in the repository. Their retention does not guarantee that the old installer accepts HW2 for downgrade. Private complete archives, BOOT/installer sources, ELF/map files, standalone fonts and printer-unique data are not published. Existing public key-free host scripts remain unchanged.

Recorded HW2 software evidence: 3070 BOOT tests, 250 installer tests, 99 ARM/static checks, 120 exact stock glyphs, 10 byte-identical rebuild artifacts. These are archived build results, not new physical tests performed during publication.

See the README and docs/v1.5 for complete Polish and English installation instructions and native-rendered screen previews.

**Hardware — potwierdzone na urządzeniu:** 29.10.2026 właściciel dodatkowo potwierdził, że ekran Hardware w stałym bootloaderze **poprawnie odczytuje rzeczywiste dane jego drukarki**. Nie jest to jedynie wynik testu modelowego. Ilustracje w instrukcji nadal zawierają jawnie syntetyczne dane przykładowe; nie są zrzutem prywatnych danych użytkownika.

**Hardware — physically confirmed:** on 29 October 2026 the owner explicitly confirmed that the permanent bootloader Hardware screen **correctly reads the actual printer data** on his device. This is an on-device confirmation, not just a model test. Manual previews still use clearly synthetic examples rather than private printer data.
