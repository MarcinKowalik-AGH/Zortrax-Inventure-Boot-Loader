# Audyt Inventure Boot v1.7 FINAL — 3 listopada 2026 r.

**Płyta:** Zortrax Inventure V9 / STM32F207. **Build:** `RELEASE 1.7`. **Status GitHub:** repozytorium publiczne, wydanie `v1.7` publiczne (`draft=false`, `prerelease=false`).

## Zestaw wydania

| Dystrybucja | Rozmiar | SHA-256 |
|---|---:|---|
| SD UPGRADE | 140880 B | `fc965284fd7fbb575ef8ed2af1b700836b51747d9d08ba1ca7b7467722fcb0f5` |
| SD FROM FACTORY V9 | 155035 B | `33846d24661e252d4f2eadc0a62bae5ab9cab81636b2acaadcc03c9a3eff23fc` |
| ST-LINK 32 KiB | 32768 B | `a8b5dbbef4e580726104cb9c812f1614f7d7cc92d978166202474cb986a57d9d` |

Wszystkie cztery załączniki GitHub Release (trzy powyższe i `SHA256SUMS.txt`) mają potwierdzone przez GitHub API rozmiary i digest SHA-256. Release jest dostępny przez [GitHub Release v1.7](https://github.com/MarcinKowalik-AGH/Zortrax-Inventure-Boot-Loader/releases/tag/v1.7).

**Zastrzeżenie dostępu:** końcowy automatyczny test anonimowego pobrania z GitHub Actions otrzymał HTTP 404. Repozytorium i wydanie mają status publiczny, a załączniki są widoczne z metadanymi i sumami, ale niezależnego anonimowego pobrania bajtów nie zaliczono jako PASS. Należy je sprawdzić również w zwykłej sesji przeglądarki bez logowania.

## Zgodność z wymaganiami

- Menu UART ma **dokładnie 115200 / 250000 / 500000 / 750000 / 1500000**, w tej kolejności.
- Domyślna prędkość **250000**, `UART on bootwait OFF`; persistencja **P4-PERSIST-r3**.
- `RELEASE 1.7` bez sufiksów RC.
- APB2/USART6 nominalnie **24 MHz**. Dzielniki OVER16: 208 / 96 / 48 / 32 / 16. Cztery ostatnie prędkości matematycznie dokładne; 115200: nominalnie 115384,615 (+0,1603%). Nie jest to pomiar oscylatora ani hosta.
- BOOT: 32504 B; **8 B** przed dziennikiem `0x08007F00–0x08007FFF`. NVM `0x08008000–0x0800FFFF` i aplikacja od `0x08010000` zachowane.
- Przejrzano oba ZIP-y SD: cztery wymagane pliki, poprawne CRC, identyczny `RESTORE.BIN` o znanym SHA-256, oba szablony kopii 32768 B.
- Oryginalna nieskalowana czcionka, Hardware, niezawijanie menu, OLED, backup, historia, recovery i pozostałe funkcje HW2 pozostają zgodnie z zakresem zmian.

## Walidacja wykonana podczas przygotowania wydania

- Testy ukierunkowane na UART, dziennik i przewijanie: **962/962 PASS**.
- Przygotowane zestawy SD: **PASS** kontroli struktury, pakietu i zgodności referencyjnego BOOT.
- Linker ARM: **32 504 B**, pełny obraz 32 768 B, zachowany dziennik.
- **Pełna regresja BOOT i instalatora:** próby uruchomione, lecz przekroczyły limit środowiska; **nie stwierdzono pełnego PASS**.
- **Test sprzętowy dokładnej 1.7:** niewykonany. Pomyślny test właściciela na jednej drukarce dotyczy wcześniejszej **1.5-HW2**.

## Integralność historii projektu

Przez API GitHub sprawdzono, że repozytorium jest publiczne, w `firmware/v1.7` są dokładnie trzy dystrybucje i dwa pliki metadanych, a katalogi `firmware/v1.4` i `firmware/v1.5` nadal zawierają poprzednie trzy binaria i ich sumy. Dokumentację wydań rozdzielono na `docs/v1.7`, `docs/v1.5` i `docs/v1.4`. Przy publikacji v1.7 zachowano poprzednie blob SHA poza zaktualizowanymi indeksami `README.md` i `docs/README.md`.

**Wniosek:** pakiety i opis są kompletne w repozytorium, binaria mają zgodne sumy. Otwarta pozostaje kwalifikacja fizyczna v1.7, ukończenie pełnej długiej regresji oraz niezależne anonimowe pobranie załączników z zewnętrznej sieci.
