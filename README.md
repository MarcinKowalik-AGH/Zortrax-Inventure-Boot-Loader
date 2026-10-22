# Inventure boot v1.3

**Binary-only installer distributions and documentation for Zortrax Inventure V9**  
**Autor / Author:** Marcin Kowalik · mkowalik@agh.edu.pl  
**Date:** 2026-10-22

[English installation guide](docs/INSTALLATION_EN.md) · [Instrukcja instalacji po polsku](docs/INSTALACJA_PL.md) · [English feature and UART reference](docs/FEATURES_AND_CONSOLE_EN.md) · [Opis funkcji i konsoli po polsku](docs/FUNKCJE_I_KONSOLA_PL.md) · [Checksums and release scope](docs/RELEASE_MANIFEST.md)

## English

Inventure boot v1.3 is an independent recovery and maintenance bootloader for the **verified Zortrax Inventure V9 with STM32F207 and 256 KiB internal Flash**. It supports a 3-second interruptible autoboot, installing and verifying compatible Inventure firmware from SD, flash and identity backups, multiple firmware files on SD, UART6 diagnostics and dumps, reset/recovery information, and service event history.

Two installation paths are documented:

1. **Upgrade v1.2 → v1.3** via the `INVENTUR.IVB` service application and two boot-sector backup slots.
2. **Factory V9 → v1.3** via the encrypted `InventureUpdate.bin` service application and the same backup mechanism.

Installation is a **two-stage operation**: first the existing bootloader installs a temporary service application into the application region; then the application installs the new bootloader after dual verified SD backups and explicit button confirmation. The original Inventure application must subsequently be restored. **Never feed the 32 KiB bootloader image directly to the application updater.**

**Release qualification:** v1.3 and factory bridge r9893 passed offline checks; **these exact builds have not yet been qualified on physical hardware**. Earlier bootloader and bridge versions were successfully tested on the owner's printers. A power failure when erasing boot sectors may require SWD/ST-Link recovery.

## Polski

Inventure boot v1.3 to niezależny bootloader serwisowy dla **zweryfikowanej płyty Zortrax Inventure V9, STM32F207, Flash 256 KiB**. Oferuje autostart po 3 sekundach z możliwością przerwania, aktualizację aplikacji z SD, weryfikację, backup Flash i danych identyfikacyjnych, listę plików, diagnostykę UART6 i historię zdarzeń.

Przewidziano **dwa odrębne warianty instalacji**: aktualizację naszego v1.2 oraz instalację na fabrycznej V9. W obu przypadkach najpierw instalowana jest aplikacja serwisowa, później następuje zweryfikowany backup dwóch sektorów bootloadera i świadomie potwierdzana instalacja nowego kodu. Na końcu trzeba przywrócić oryginalną aplikację Inventure.

**Uwaga:** wydanie v1.3 i nowy instalator r9893 mają zaliczone testy komputerowe, ale **nie są jeszcze osobno sprawdzone sprzętowo**. Przerwanie zapisu sektorów 0–1 może wymagać ratowania przez ST-Link. Stosować tylko na zgodnej płycie i przy stabilnym zasilaniu.

## Distribution policy / Zasady publikacji

**Binary and installation packages only. No bootloader/installer C or assembly sources, build system, ELF, map, disassembly, private MCU dumps, OTP, UID or customer calibration data are published.**

No affiliation with, authorization from, or endorsement by Zortrax is implied. This is a third-party maintenance project for equipment owned by its users. Original manufacturer's firmware may be subject to separate copyright and license terms; check those terms before redistribution.

See the detailed guides for file layout, expected messages, complete console commands and safety checks.
