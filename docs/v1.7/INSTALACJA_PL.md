# Zortrax Inventure boot v1.7 — FINAL (RELEASE 1.7)

**Wydanie:** 3 listopada 2026. **Cel:** wyłącznie Inventure V9, STM32F207, 256 KiB Flash. **Stan testu sprzętowego:** brak odbioru tej konkretnej kompilacji; wcześniej zweryfikowano na jednej drukarce v1.5-HW2 i ekran Hardware. Pliki v1.7 są kandydatem FINAL po walidacji programowej, lecz nazwa FINAL nie zastępuje odbioru fizycznego.

## Pięć prędkości UART/P4

W `Diagnostics → UART → P4 baud rate` są **wyłącznie, w tej kolejności**:

`115200 · 250000 · 500000 · 750000 · 1500000`

**115200 jest pierwsze dla kompatybilności; domyślne pozostaje 250000.** Konsola używa 8N1. `UART on bootwait` ma wartości OFF/ON, domyślnie OFF: sondowanie przez Orange Pi nie przerywa pięciosekundowego autostartu. ON dopuszcza tylko pełne, rozpoznane komendy diagnostyczne po READY. P4-PERSIST-r3 zapisuje baud i OFF/ON niezależnie w istniejących 256 B BOOT; pełne ponowne wgranie BOOT przywraca 250000/OFF.

Dzielniki USART6 oblicza się dla zegara **APB2 24 MHz**, uzyskanego z HSI16 i PLL (PLLM=16, PLLN=192, PLLP=8). Nominalny błąd dzielnika (bez tolerancji HSI i hosta):

| Menu | BRR (OVER16) | Nominalny baud | Błąd |
|--:|--:|--:|--:|
| 115200 | 208 | 115384,615 | +0,1603% |
| 250000 | 96 | 250000 | 0% |
| 500000 | 48 | 500000 | 0% |
| 750000 | 32 | 750000 | 0% |
| 1500000 | 16 | 1500000 | 0% |

To dokładność nominalna dzielnika, nie pomiar stabilności fizycznego UART. Starsze, ukryte ustawienia dziennika mogą być odczytane z kompatybilnych wpisów; nie ma ich w menu.

## Zachowane funkcjonalności

Oryginalna nieskalowana czcionka r0323, Hardware (OTP/NVM), menu bez zawijania i z przypiętym Back, częściowe odświeżanie OLED, konsola P4, aktualizacja APP, backup, historia, recovery, fizyczne potwierdzenia i mapy pamięci pozostały. Nie portowano sterowników M300. Wersja jest `RELEASE 1.7` bez dodatkowych sufiksów identyfikatora.

## Trzy drogi instalacji

**1. UPGRADE:** dla zgodnego własnego BOOT. Rozpakuj `_SD_UPGRADE.zip` do katalogu głównego FAT32, nie kopiuj ZIP wprost. Pliki: `INVENTUR.IVB`, `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN`. W BOOT wybierz i zweryfikuj `INVENTUR.IVB`, instaluj po potwierdzeniu **OK+UP 2 s**; uruchom pośrednik po **OK+DOWN 2 s**. Pośrednik: wykonaj dwie zweryfikowane kopie aktualnego BOOT, potem osobno zaakceptuj wymianę BOOT (puszczenie przycisków → pojedynczy OK i puszczenie → **OK+UP 5 s**). Po restarcie nie uruchamiaj automatycznie pośrednika: **jawnie przywróć aplikację** przez wybranie `RESTORE.BIN` i kontrolę `VERIFY`. Pierwszy start: 250000/OFF.

**2. FROM FACTORY:** tylko dla dokładnie rozpoznanego fabrycznego V9, poprawnych warunków RDP0/WRP i możliwości zapisu. Rozpakuj `_SD_FACTORY_V9.zip` do FAT32; zawiera `InventureUpdate.bin`, `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN`. Fabryczny updater instaluje pośrednik w APP. Następnie obowiązują procedury dwóch kopii, potwierdzenia i jawnego przywrócenia APP jak wyżej. Odmowa wymiany BOOT nie przywraca APP automatycznie.

**3. ST-LINK:** wyłącznie dla dostępnej i rozpoznanej własnej płyty V9. Zabezpiecz i zweryfikuj dwa odczyty pełnych 256 KiB oraz dane identyfikacyjne. Zapisz plik `_STLINK_32KiB_0x08000000.bin` pod `0x08000000`, kasując **tylko sektory 0–1**. Po zapisie porównaj readback BOOT i wszystkie bajty od `0x08008000` z kopią. Bez Mass Erase, Read Unprotect ani zmiany Option Bytes. Ta metoda nie zastępuje APP.

**Uwaga:** `RESTORE.BIN` przywraca stockową aplikację **Zortrax 1.6.1/r0323**, a nie wcześniejszego Klippera. Paczka BOOT nie instaluje i nie konfiguruje hosta/MCU Klippera. Prędkość po stronie hosta i aplikacji trzeba dostosować osobno.

## Weryfikacja

Źródła zbudowano do 32 504 B + wypełnienie FF; pełny BIN ma 32 768 B. Przed dziennikiem P4 zostaje **8 B**. Dziennik `0x08007F00–0x08007FFF`, NVM `0x08008000–0x0800FFFF`, APP od `0x08010000`. Testy nawigacji/baud/P4 wykonane w tej sesji: **962/962 PASS**; sprawdzenie obu zestawów SD: PASS, weryfikacja wspólnego obrazu BOOT i referencji APP: PASS. Pełne, długie zestawy regresji były uruchamiane, ale przekroczyły czas wykonania środowiska; nie są raportowane jako pełny PASS. Odbiór na fizycznej drukarce — OTWARTY.

Pliki wydania i ich sumy SHA-256: [SHA256SUMS](../../firmware/v1.7/SHA256SUMS.txt). Archiwa poprzednich wydań pozostają w `firmware/v1.5`, `firmware/v1.4`, a ich instrukcje odpowiednio w `docs/v1.5` i `docs/v1.4`.
