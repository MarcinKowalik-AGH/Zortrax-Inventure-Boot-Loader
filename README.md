# Inventure boot v1.5 — RELEASE 1.5-HW2

**Zortrax Inventure V9 · STM32F207 · 256 KiB Flash**  
Autor / Author: **Marcin Kowalik**, mkowalik@agh.edu.pl. Wydanie / release: **29.10.2026**.

## Pobierz bieżącą v1.5 / Download current v1.5

| Stan drukarki / Current state | Właściwy plik / Correct package |
|---|---|
| Rozpoznany własny Inventure boot, również v1.4 | **[UPGRADE](firmware/v1.5/Inventure_boot_v1.5_HW2_STOCK_FONT_2026-10-29_SD_UPGRADE.zip)** |
| Dokładnie rozpoznany oryginalny BOOT V9, spełnione warunki zapisu | **[FROM FACTORY](firmware/v1.5/Inventure_boot_v1.5_HW2_STOCK_FONT_2026-10-29_SD_FACTORY_V9.zip)** |
| Dostęp SWD / ST-Link | **[ST-LINK — 32 KiB pod 0x08000000](firmware/v1.5/Inventure_boot_v1.5_HW2_STOCK_FONT_2026-10-29_STLINK_32KiB_0x08000000.bin)** |

[Publiczne wydanie v1.5](https://github.com/MarcinKowalik-AGH/Zortrax-Inventure-Boot-Loader/releases/tag/v1.5) · [SHA-256](firmware/v1.5/SHA256SUMS.txt) · [Manifest](docs/v1.5/RELEASE_MANIFEST.md)

## Dokumentacja — zawsze według wersji / Versioned documentation

**[Pełna dokumentacja v1.5](docs/v1.5/README.md)** · **[Instrukcja instalacji PL](docs/v1.5/INSTALACJA_PL.md)** · **[English installation](docs/v1.5/INSTALLATION_EN.md)**

[Funkcje i Hardware PL](docs/v1.5/FUNKCJE_I_KONSOLA_PL.md) · [Features and console EN](docs/v1.5/FEATURES_AND_CONSOLE_EN.md) · [Przykłady P4 PL](docs/v1.5/KONSOLA_P4_PRZYKLADY_PL.md) · [P4 examples EN](docs/v1.5/P4_UART_EXAMPLES_EN.md) · [Publiczne narzędzia PC](tools/README.md)

| Wersja | Dokumentacja | Pliki |
|---|---|---|
| **1.5 — aktualna / current** | [docs/v1.5](docs/v1.5/README.md) | [firmware/v1.5](firmware/v1.5) |
| 1.4 — archiwum / archive | [docs/v1.4](docs/v1.4/README.md) | [firmware/v1.4](firmware/v1.4) |
| 1.3 — starsze archiwum / legacy | [docs/v1.3](docs/v1.3/README.md) | [SD_INSTALLATION](SD_INSTALLATION) |

[Indeks wszystkich wersji](docs/README.md) · [Audyt repozytorium](docs/v1.5/AUDYT_REPOZYTORIUM_PL.md)

## Potwierdzenie na urządzeniu / Hardware feedback

**29.10.2026 właściciel potwierdził instalację na jednej drukarce i poprawny odczyt rzeczywistych danych w Hardware stałego bootloadera.** Nie jest to wyłącznie wynik modelu. Binaria są identyczne z przetestowanymi; nie zmieniono ich podczas porządkowania dokumentacji. To potwierdzenie jednego urządzenia, nie odrębny odbiór każdej trasy, prędkości ani awarii zasilania.

**The owner confirmed installation on one printer and correct reading of its actual data in permanent BOOT Hardware.** This is an on-device report. Published firmware is unchanged, not rebuilt for the documentation audit. Synthetic native-rendered manual previews are not photographs or private device dumps.

Instalator zachowuje wcześniejszy napis `V1.5 HW2 - HW UNTESTED` oraz identyfikację rodziny r9898/UI-MEM1. To historyczne teksty przetestowanego binarium, nie aktualna ocena poprawności Hardware. Wersję pakietu identyfikuje pełne SHA-256 i `RELEASE 1.5-HW2`.

## Funkcje v1.5-HW2 / Features

Oryginalna nieskalowana czcionka r0323 w BOOT i instalatorze; Hardware z modelem, wersją sprzętu i numerem z OTP oraz **Print time** z NVM; menu bez zawijania, przypięty Back i pamiętane okno listy; częściowe odświeżanie OLED; bezstratna kompresja tekstów z 80 B zapasu przed dziennikiem P4. Zachowane formaty aktualizacji, kopie, historia, recovery i trwała prędkość P4.

![Ekrany v1.5-HW2](docs/v1.5/images/overview.png)

*Rendery kodu C; dane Hardware są syntetyczne. / Native C renders with synthetic device data.*

## Przed wgraniem / Before installation

Oba ZIP-y SD zawierają **cztery pliki** do głównego katalogu FAT32. Pośrednik zastępuje tymczasowo APP, wykonuje dwie kopie BOOT i wymaga osobnego potwierdzenia podmiany. **Po instalacji przywróć APP przez RESTORE.BIN (Zortrax 1.6.1/r0323).** Nie jest to kopia dowolnego poprzedniego firmware.

ST-Link zapisuje **tylko sektory 0–1**, z kontrolą zachowania NVM i APP. Nie używaj Mass Erase, Read Unprotect ani zmian Option Bytes do obejścia odmowy. Droga factory wymaga rozpoznanego oryginału, RDP0 i zapisywalnych sektorów BOOT/APP; nie wyłącza ochrony. Wymiana BOOT resetuje zapis P4 do **250000, 8N1**, zwykła aktualizacja APP go zachowuje.

Publiczne narzędzia hosta nie zawierają kluczy odszyfrowywania ani funkcji odtwarzania tail20. Nie publikujemy prywatnego KOMPLETU, źródeł BOOT/instalatora, ELF/map ani indywidualnych zrzutów drukarki. Zachowanie v1.4 nie oznacza gwarantowanego downgrade z HW2. Tag v1.5 pozostaje oryginalnym snapshotem wydania; aktualne instrukcje są na `main`.
