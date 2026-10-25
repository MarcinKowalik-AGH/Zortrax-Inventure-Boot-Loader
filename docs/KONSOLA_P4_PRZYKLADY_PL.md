# Konsola P4 — polecenia, oryginalny firmware, odszyfrowany firmware i Klipper

**Dotyczy:** Inventure boot v1.4 `P4-PERSIST-r2` (V9 / STM32F207 / 256 KiB Flash). Instrukcja uzupełniająca wydanie z 25.10.2026.  
[Projekt](../README.md) · [Pełny opis funkcji](FUNKCJE_I_KONSOLA_PL.md) · [Instalacja bootloadera SD / ST-Link](INSTALACJA_PL.md) · [English](P4_UART_EXAMPLES_EN.md)

> Konsola `INV>` działa **wyłącznie w naszym bootloaderze**, przed uruchomieniem aplikacji. Nie jest konsolą G-code ani konsolą oryginalnego Zortraxa. `SDUPDATE` i `UARTUPDATE` wymieniają tylko aplikację **APP od 0x08010000**, nie sam BOOT, NVM, OTP czy Option Bytes. Przed programowaniem wykonaj i zweryfikuj kopię pamięci. Nie używaj Mass Erase, zmiany RDP ani Option Bytes do obejścia odmowy.

## 1. Podłączenie do P4

Port P4 to **USART6**, gdzie **PG14 = TX drukarki**, **PG9 = RX drukarki**. Łącz TX drukarki z RX adaptera, RX drukarki z TX adaptera oraz GND z GND. Obowiązuje **TTL 3,3 V**, a nie 5 V lub RS-232. Nie zasilaj drukarki przewodem VCC z adaptera. Numerację i orientację styków P4 sprawdź na własnej płycie.

Po resecie przerwij **5-sekundowy autostart** przyciskiem lub znakiem UART. Terminal ustaw na **8N1, bez kontroli przepływu**. Prędkość zależy od zapisanej wartości: **19200 / 57600 / 115200 / 250000 / 500000**. Domyślnie po instalacji BOOT jest **250000**. Awaryjnie trzymaj **UP+DOWN przy starcie**, aby na jedno uruchomienie uzyskać 250000 bez kasowania zapisanego ustawienia.

Przykład dla macOS (podmień nazwę urządzenia i baud na rzeczywiste):

```sh
python3 -m pip install pyserial
python3 -m serial.tools.miniterm /dev/cu.TWOJ_PORT 250000 --eol LF
```

Na Linux port może mieć nazwę `/dev/ttyUSB0`, na Windows `COM5`. Bootloader domyślnie wykonuje echo — wyłącz lokalne echo terminala. Miniterm zamyka się przez **Ctrl+]**. Nie pozostawiaj terminala otwartego równolegle z programem przesyłającym firmware.

Przykładowa próba bez zapisu (fragmenty odpowiedzi są poglądowe):

```text
INV> PING
PONG 250000 8N1
DONE OK
INV> INFO
... BUILD P4-PERSIST-r2 ...
... P4_BAUD 250000 8N1 SAVED 250000 ...
INV> HELP
... lista komend ...
DONE OK
```

## 2. Spis komend

| Polecenie w konsoli | Działanie |
|---|---|
| `HELP`, `INFO`, `PING` | Pomoc, wersje/stany, test `PONG` |
| `VERIFY` | Kontrola obrazu APP aktualnie zapisanego we Flash |
| `LIST` | Lista plików firmware z głównego katalogu SD (do 16 pozycji) |
| `SELECT n` | Wybór pozycji z `LIST`, **numeracja od zera** |
| `SELECT AUTO` | Reset wyboru na standardowe nazwy plików |
| `SDCHECK` | Walidacja wybranego pakietu na karcie — bez zapisu |
| `SDUPDATE` | Zapis APP po fizycznym **OK+UP przez 2 s** |
| `UARTCHECK N` | Kontrola pakietu o długości N dostarczanego ramkami `IBD1` |
| `UARTUPDATE N` | Odbiór i zapis pakietu `IBD1`, po **OK+UP przez 2 s** |
| `BOOT` | Uruchomienie APP po **OK+DOWN przez 2 s** |
| `REBOOT` | Reset MCU |
| `MENU`, `HOME`, `BACK` | Powrót do głównego menu; `BACK` nie cofa o jedną stronę |
| `ECHO ON`, `ECHO OFF` | Echo znaków |
| `BACKUP` | Kopia całych 256 KiB Flash i informacji urządzenia na SD |
| `DUMP FLASH`, `DUMP NVM`, `DUMP OTP`, `DUMP UID`, `DUMP OPTIONS` | Tylko odczyt w formie tekstowych rekordów HEX z CRC32 i końcowym SHA-256 |
| `CARDINFO`, `DIAG`, `DISPLAY` | Karta SD, wejścia przycisków/GPIO, wzory OLED |
| `RESETINFO`, `RECOVERY CLEAR` | Informacje o resetach / świadome czyszczenie blokady recovery |
| `LOG`, `LOGSAVE` | Historia zdarzeń na UART lub do przygotowanego pliku |

Sukces to zwykle `DONE OK`, odmowa `ERROR <kod>`; podczas operacji mogą być `PHASE` i `PROGRESS`. `DONE ALREADY_INSTALLED` oznacza pominięty zapis identycznego obrazu. **Nie ma komend** `BAUD`, `SELECT RESTORE.BIN`, `ERASE`, `WRITE 0x...` ani `M997`. Zmiana baud jest tylko w OLED: `Diagnostics → UART → P4 baud rate`.

## 3. Przygotowanie kopii pamięci

Aby `BACKUP` zadziałał, karta FAT32 musi mieć w katalogu głównym **wcześniej utworzone i wypełnione 0xA5** pliki `INVFLASH.BIN` (**262144 B**) i `INVINFO.BIN` (**1024 B**). Opcjonalny `LOGSAVE` używa `INVLOG.BIN` (**4096 B**). **Nie zastępuj prawdziwych kopii szablonami**. Po `BACKUP` potwierdź na panelu **OK+UP 2 s**, sprawdź poprawny wynik i przenieś kopie na niezależne nośniki. Nie publikuj NVM/OTP/UID urządzenia.

```text
INFO
VERIFY
BACKUP
... potwierdź OK+UP 2 s na drukarce ...
... BACKUP VERIFIED: INVFLASH.BIN + INVINFO.BIN ...
DONE OK
```

`DUMP FLASH` nie wysyła surowego binarium, lecz `BEGIN_DUMP`, `DATA <offset> <crc32> <dane_hex>`, `END_DUMP SHA256`. Odbiorca musi sprawdzić ciągłość offsetów, CRC32 wszystkich fragmentów, SHA-256 i długość. Samo przemianowanie logu `.txt` na `.bin` nie daje prawidłowej kopii.

## 4. Przykład A — oryginalny zaszyfrowany `InventureUpdate.bin` (ZRTX)

**Wariant z kartą SD i sterowaniem z P4.** Plik producenta musi być autentycznym, rozpoznanym kontenerem `ZRTXUINV`. Bootloader dopuszcza tylko **osiem dokładnie znanych obrazów aplikacji** i sprawdza ich integralność/wektory. Sam napis wersji nie wystarcza.

1. Włóż kartę FAT32 z obsługiwanym `InventureUpdate.bin` w katalogu głównym, bez konkurencyjnych pakietów.
2. Wejdź do konsoli bootloadera i wybierz plik **rzeczywistym numerem** z `LIST`.
3. Zweryfikuj `SDCHECK`; zapisz `SDUPDATE` tylko jeśli walidacja się powiodła.
4. Zweryfikuj obecny Flash komendą `VERIFY`, a potem uruchom `BOOT`.

```text
LIST
... 0 InventureUpdate.bin ...
SELECT 0
SDCHECK
... DONE OK ...
SDUPDATE
... zwolnij przyciski, OK+UP 2 s ...
... DONE OK ...
VERIFY
... INSTALLED ... 
DONE OK
BOOT
... OK+DOWN 2 s ...
```

Numer 0 to **przykład**, nie gwarantowana pozycja. `SDUPDATE` aktualizuje aplikację, a nie sektory BOOT.

**Zaszyfrowany ZRTX przez UART:** publiczne [`tools/vendor_tool.py`](../tools/vendor_tool.py) **nie zawiera klucza AES** i nie odszyfrowuje `InventureUpdate.bin`. Sam `ibtool.py serial` przyjmuje tylko poprawnie przygotowany `.IVB`, a nie zaszyfrowany pakiet. Bezpieczna droga dla zaszyfrowanego pliku to powyższa instalacja z **SD** (bootloader sam rozpoznaje i sprawdza wspierany obraz).

Można **bez odszyfrowywania** podejrzeć jedynie metadane zewnętrznego kontenera:

```sh
python3 tools/vendor_tool.py InventureUpdate.bin
# Wypisuje tylko zewnętrzną rewizję i rozmiar.
# --ivb-out przy zaszyfrowanym wejściu zostanie świadomie odrzucone.
```

Aby przesłać oryginalną aplikację przez UART, należy **posiadać już odszyfrowany, znany obraz APP** i spakować go do `.IVB` publicznym narzędziem opisanym w przykładzie B. W repozytorium nie publikujemy klucza odszyfrowywania, klucza HMAC, danych `tail20` ani żadnego programu je wyliczającego.

## 5. Przykład B — odszyfrowany, oryginalny obraz APP

Odszyfrowana aplikacja Zortraxa to nie dowolny plik `.bin`. Znany format zawiera wektory APP dla `0x08010000`, wewnętrzny magic `0x12345678` w offsetcie `0x1C`, rozmiar pod `0x20` i rewizję `rNNNN` od `0x24`; może mieć HMAC oraz kanoniczne wypełnienie `0xCD`. Nadal obowiązuje allowlista **ośmiu** SHA-256. **Pełny dump Flash 262144 B nie jest obrazem APP!**

Dla zgodnego `application_r0323.bin` lub już sprawdzonego `RESTORE.BIN` umieszczonego w głównym katalogu SD:

```text
LIST
SELECT 1
SDCHECK
SDUPDATE
VERIFY
BOOT
```

`SELECT 1` znów jest wyłącznie przykładem; odczytaj numer z `LIST`. **RESTORE.BIN należy wybrać jawnie**, nie jest wybierany przez `SELECT AUTO`. Potwierdzenia i weryfikacja jak powyżej.

**Przesyłanie przez UART bez sekretów:** oba skrypty są teraz publiczne: [`tools/vendor_tool.py`](../tools/vendor_tool.py) i [`tools/ibtool.py`](../tools/ibtool.py). Pierwszy przyjmuje **już odszyfrowaną** aplikację, sprawdza jej SHA-256 względem ośmiu rozpoznanych obrazów i opakowuje ją w IVB. Jeżeli plik zawiera **kompletny oryginalny payload wraz z istniejącym tail i paddingiem**, narzędzie zachowa go wyłącznie po zgodności pełnego SHA-256 z archiwalnym wzorcem. Nie generuje ani nie sprawdza HMAC za pomocą tajnego klucza.

```sh
python3 -m pip install pyserial
python3 tools/vendor_tool.py application_r0323.bin --ivb-out STOCK_RAW_R0323.IVB
python3 tools/ibtool.py inspect STOCK_RAW_R0323.IVB
# Bez zapisu: UARTCHECK
python3 tools/ibtool.py serial STOCK_RAW_R0323.IVB --port /dev/cu.TWOJ_PORT --baud 250000
# Dopiero po pomyślnym teście: UARTUPDATE + potwierdzenie OK+UP 2 s
python3 tools/ibtool.py serial STOCK_RAW_R0323.IVB --port /dev/cu.TWOJ_PORT --baud 250000 --update
```

**Istotne rozróżnienie:** gdy plik wejściowy zawiera *samą* surową APP (bez oryginalnego tail), wynik jest poprawnym **własnym IVB z manifestem** dla tego samego kodu aplikacji, **nie** bajtowo identycznym pełnym obrazem fabrycznym. Publiczny skrypt nie odtwarza tail20. Nie traktuj tej drogi jako osobno potwierdzonego testu sprzętowego. Dla oryginalnej, kanonicznej postaci firmware użyj sprawdzonego `RESTORE.BIN` lub autentycznego pakietu ZRTX bezpośrednio z SD. Nie usuwaj HMAC/paddingu z kompletnego obrazu i nie przesyłaj pełnego dumpa Flash jako APP.

## 6. Przykład C — własna aplikacja, np. Klipper MCU

To **nie jest instrukcja instalacji zwykłego, uniwersalnego Klippera**. Działające bez sekretów [`tools/ibtool.py`](../tools/ibtool.py) jest dostępne w tym repozytorium. Potrzebny jest obraz przygotowany dla **STM32F207, Inventure V9**, z właściwymi zegarami, mapą GPIO, obsługą sprzętu i bezpieczeństwa, linkowany do **`0x08010000`**. Sam plik o nazwie `klipper.bin` nie wystarcza.

Bootloader obsługuje niezaszyfrowany format **`INVB001`** z nagłówkiem 64 B, `target=0x32463956`, `base=0x08010000`, długością i SHA-256. Surowa APP musi mieć **8–196352 B**, MSP w zakresie SRAM 128 KiB wyrównany do 8 i adres Reset Handler Thumb wewnątrz payloadu. Te warunki potwierdzają *strukturę*, nie poprawność termiki i napędów.

Na komputerze, korzystając z publicznego [`tools/ibtool.py`](../tools/ibtool.py):

```sh
python3 tools/ibtool.py pack klipper.bin KLIPPER_V9.IVB
python3 tools/ibtool.py inspect KLIPPER_V9.IVB
```

Jeżeli program odrzuca rozmiar lub wektory, **popraw konfigurację kompilacji/linkowania** — nie fałszuj wektorów hex-edytorem.

**SD + sterowanie P4:** skopiuj `KLIPPER_V9.IVB` do katalogu głównego i wpisz `LIST`, następnie `SELECT n` według faktycznego indeksu, `SDCHECK`, `SDUPDATE` (OK+UP 2 s), `VERIFY`, `BOOT` (OK+DOWN 2 s). Przy `VERIFY` własnej APP może pojawić się `CUSTOM_MANIFEST`.

**Bez SD, transmisja przez P4 z komputera:**

```sh
python3 tools/ibtool.py serial KLIPPER_V9.IVB --port /dev/cu.TWOJ_PORT --baud 250000
# po poprawnym teście bez zapisu:
python3 tools/ibtool.py serial KLIPPER_V9.IVB --port /dev/cu.TWOJ_PORT --baud 250000 --update
```

Host odpowiada na żądania `READ <offset> <liczba_bajtów>` binarnymi ramkami **IBD1 + CRC32**. Wpisanie samego `UARTUPDATE N` i wklejenie `klipper.bin` do terminala **nie działa**. Klipper po uruchomieniu przejmuje UART we własnym protokole; prompt `INV>` znika. Projekt portu Klippera ma testy software, ale nie można traktować samej poprawnej instalacji jako potwierdzenia kompletnego, bezpiecznego sterowania grzałkami i mechaniką.

**Powrót do oryginału:** przerwij autostart naszego bootloadera po restarcie, potem zainstaluj rozpoznaną fabryczną APP z SD/UART (kontrola → zapis → `VERIFY` → `BOOT`). Nie ma automatycznego A/B rollbacku. Przed pierwszym uruchomieniem alternatywnej APP zabezpiecz obraz stock i NVM.

## 7. Ograniczenia i komunikaty błędów

| Odpowiedź | Co oznacza |
|---|---|
| `NOTFOUND`, `AMBIGUOUS_FILES` | Brak pliku, nadmiar kandydatów; użyj `LIST` i `SELECT n` |
| `FORMAT`, `RANGE`, `VECTOR` | Zły format, adres, rozmiar lub wektory — nie wgrywaj |
| `HASH`, `CRC`, `CHANGED` | Niezgodność integralności lub transferu |
| `VENDOR_UNKNOWN_IMAGE` | Nieznany stock — odmowa, nie omijaj kontroli |
| `CONFIRM`, `BUTTONS` | Brak prawidłowego potwierdzenia na panelu |
| `HARDWARE`, `FLASH`, `READONLY` | Niespełnione warunki urządzenia/zapisu |
| `NO_COMMIT`, `HW_WATCHDOG` | Brak ważnego manifestu/APP lub stan recovery |
| `DONE ALREADY_INSTALLED` | Weryfikacja zgodności obrazu i pominięty zapis |

**Zasada końcowa:** po zapisie zawsze `VERIFY` przed `BOOT`. Nie zmieniaj RDP, Option Bytes, BOOT ani banków fabrycznego NVM, żeby obchodzić błąd. Przykłady opracowano na podstawie rzeczywistych narzędzi i kodu wydania r2; **nie są nowymi testami fizycznymi wszystkich trzech przypadków**.
