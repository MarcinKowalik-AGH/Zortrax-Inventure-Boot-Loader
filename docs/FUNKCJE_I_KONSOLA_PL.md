# Inventure boot v1.3 — menu, funkcje i konsola UART

**Autor:** Marcin Kowalik · mkowalik@agh.edu.pl. Płyta referencyjna: Inventure V9, STM32F207, Flash 256 KiB.

**Potwierdzenie sprzętowe użytkownika:** pomyślnie wykonano zarówno **aktualizację Inventure boot v1.2 → v1.3**, jak i **instalację na fabrycznej drukarce z bootloaderem Zortraxa v1.0**, przywrócenie programu i jego uruchomienie. Nie oznacza to jeszcze fizycznego przetestowania każdej nowej funkcji diagnostycznej v1.3.

## Start i przyciski

Po włączeniu wyświetla się **odliczanie 3 sekund**. Bez naciśnięcia przycisku następuje weryfikacja i automatyczny start poprawnej aplikacji. **GÓRA**, **OK** lub **DÓŁ** w trakcie odliczania zatrzymuje start i otwiera menu. Niepoprawna aplikacja lub aktywny recovery powodują pozostanie w menu. Sama obecność aktualizacji na karcie **nie uruchamia jej automatycznie**.

W menu: **GÓRA = poprzednia pozycja, DÓŁ = następna, OK = zatwierdzenie**. W każdym podmenu jest opcja **Back** („Powrót”). Zapis aplikacji wymaga dodatkowego potwierdzenia **OK + GÓRA przez 2 s**, a ręczny start **OK + DÓŁ przez 2 s**. Kieruj się również dokładnymi komunikatami widocznymi na OLED.

## Opcje menu

| Dział | Możliwości |
| --- | --- |
| **Start application** | Walidacja i ręczny start programu Zortraxa; oryginalna aplikacja może uruchamiać ruch i grzanie |
| **Firmware on SD** | Lista do 16 zgodnych plików w katalogu głównym, wybór, sprawdzanie integralności, aktualizacja wybranego obrazu z potwierdzeniem, pomijanie identycznego firmware |
| **Verify installed** | Odczytowa kontrola obecnej aplikacji |
| **Backup / Recovery** | Kopia głównej Flash 256 KiB oraz danych identyfikacyjnych do przygotowanych plików SD, odczytowa weryfikacja kopii |
| **Diagnostics** | Przyczyny resetu, diagnostyka SD, test przycisków i wzorów OLED, odczyt wejść GPIO, test UART |
| **System information / About** | Nazwa, wersja, autor, e-mail, warunki sprzętowe i limit aplikacji |
| **Restart / Back** | Restart lub powrót do poprzedniej strony menu |

Na OLED tekst jest po angielsku i używa jednolitej małej czcionki; nagłówek `Inventure boot v1.3 © Marcin Kowalik`.

## Oryginalne firmware i bezpieczny zapis

Obsługiwane są pakiety Zortraxa `InventureUpdate.bin` z AES, zgodne pliki aplikacji `INVENTUR.BIN` i format `.IVB`. Bootloader sprawdza strukturę, kryptografię i integralność **przed** kasowaniem aplikacji. Po zapisie sprawdza wynik. Nie programuje przy tym sektorów 0–1, fabrycznych NVM 2–3, OTP i Option Bytes. Jeśli firmware jest identyczne z zainstalowanym, zgłasza pominięcie bez zbędnego kasowania.

**Ważne:** zwykłe `SDUPDATE` służy do aplikacji pod `0x08010000`, a nie do bezpośredniego wgrywania BIN bootloadera pod `0x08000000`.

## Pliki serwisowe FAT32

| Plik | Rozmiar | Funkcja |
| --- | ---: | --- |
| `INVFLASH.BIN` | 262 144 B | Aktualna główna pamięć Flash |
| `INVINFO.BIN` | 1 024 B | UID, OTP, opcje i kontrola spójności |
| `INVLOG.BIN` | 4 096 B | Eksport dziennika zdarzeń |

Skopiowanie samych szablonów nie tworzy backupu. Dopiero pozytywny zapis i weryfikacja na drukarce oznaczają gotową kopię. Zabezpiecz wykonane kopie poza kartą i **nie publikuj** NVM, UID, OTP ani prywatnych danych sprzętu.

## Przyczyny restartów i tryb recovery

`RESETINFO` pokazuje flagi resetu, licznik uruchomień i stan recovery. **Trzy resety watchdogiem po zapamiętanym przekazaniu sterowania** mogą włączyć blokadę autostartu. Zatrzask można wyczyścić świadomie poleceniem `RECOVERY CLEAR`. Zwykłe odłączenie zasilania nie jest automatycznie zaliczane jako awaria. Mechanizm nie rozpoznaje wszystkich możliwych zawieszeń.

Historia obejmuje do **24 zdarzeń** w backup SRAM, zabezpieczonych CRC; zaniku pełnego zasilania może nie przetrwać. `LOGSAVE` zapisuje ją do przygotowanego `INVLOG.BIN`.

## Połączenie konsoli UART6

Złącze P4: **C = PG14/TX**, **D = PG9/RX**, **G = GND**. Poziomy logiki **3,3 V**, nie 5 V. Na STLINK-V3SET / MB1440C port VCP ma dwa sygnały: **CN3 pin 1 T_VCP_TX → P4 C**, **CN3 pin 2 T_VCP_RX → P4 D** i wspólną masę. Nie łącz pinu VCC adaptera TTL z zasilaniem płyty.

Prędkość **250000 baud, 8N1, bez kontroli przepływu**, koniec wiersza LF. Na Macu, po wykryciu właściwego portu:
```bash
python3 -m serial.tools.miniterm /dev/cu.usbmodem14203 250000 --eol LF
```
Koniec sesji: **Ctrl+]**. Konsola odsyła znaki (prompt `INV>`), więc nie włączaj drugiego lokalnego echo. Po uruchomieniu fabrycznej aplikacji konsola serwisowa przestaje odpowiadać, ponieważ następuje przekazanie sterowania.

## Komendy UART

| Komenda | Opis |
| --- | --- |
| `INFO` | Nazwa, wersja, autor i e-mail, stan sprzętu |
| `VERIFY` | Weryfikacja aplikacji bez zapisu |
| `SDCHECK` | Sprawdzenie obrazu na SD bez zapisu |
| `SDUPDATE` | Żądanie instalacji aplikacji po fizycznym potwierdzeniu |
| `BOOT` | Ręczny start poprawnej aplikacji po potwierdzeniu |
| `REBOOT` | Restart |
| `RESETINFO` | Reset i recovery |
| `RECOVERY CLEAR` | Świadome wyzerowanie blokady recovery |
| `PING` | Diagnostyka UART |
| `LOG` | Historia zdarzeń |
| `LOGSAVE` | Zapis historii na SD |
| `DUMP FLASH` | Eksport 256 KiB Flash po UART z kontrolą CRC/SHA |
| `DUMP NVM` | Eksport NVM |
| `DUMP OTP` | Eksport OTP — dane specyficzne dla urządzenia |
| `DUMP UID` | Odczyt identyfikatora MCU |
| `DUMP OPTIONS` | Odczyt opcji ochrony |
| `UARTCHECK <length>` | Kontrola pakietu przesyłanego protokołem ramkowym |
| `UARTUPDATE <length>` | Żądanie aktualizacji przesłanym pakietem, nadal wymagające potwierdzenia |

Polecenia `DUMP` zwracają **dane binarne w ramkach**, dlatego do zapisu użyj programu obsługi protokołu zamiast kopiować znaki z miniterm. Możliwości różnych pozycji menu i komend mogą różnić się nieznacznie; komunikaty na OLED są nadrzędne przy potwierdzaniu operacji.

**Nie kasuj sektorów 0–1 bez kopii i możliwości naprawy przez SWD.** Dwa pliki backupu na jednej SD nie zabezpieczają przed awarią tej karty.
