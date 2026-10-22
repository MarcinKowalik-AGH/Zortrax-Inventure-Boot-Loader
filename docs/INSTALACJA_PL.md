# Inventure boot v1.3 — instalacja przez SD (polski)

Autor: **Marcin Kowalik** — mkowalik@agh.edu.pl

## Status prób sprzętowych

**Obie drogi instalacji zostały pomyślnie przetestowane na prawdziwych drukarkach Inventure:**
- **upgrade z naszego Inventure boot v1.2 do v1.3**;
- **instalacja na drukarce z fabrycznym bootloaderem Zortraxa v1.0**, przywrócenie aplikacji i jej prawidłowe uruchomienie.

Potwierdza to oba scenariusze instalowania na przetestowanych egzemplarzach, ale nie stanowi gwarancji dla wszystkich rewizji płyt ani potwierdzenia każdej dodatkowej funkcji diagnostycznej. Docelowy sprzęt: **Inventure V9, STM32F207, 256 KiB Flash**.

## Pobierz paczkę instalacyjną na SD

Oba archiwa znajdują się w publicznym [katalogu SD_INSTALLATION](../SD_INSTALLATION/README.md).

- **Drukarka z naszym Inventure boot v1.2:** [pobierz ZIP aktualizacyjny v1.2 → v1.3](../SD_INSTALLATION/01_UPGRADE_v1.2_to_v1.3/Inventure_boot_v1.3_SD_Z_v1.2_JEDNA_KARTA.zip) — SHA-256 `1acb7a734263fd38046f89c4cb6e510454f69e5701885fa1d459f1f805e0ca9a`.
- **Drukarka z fabrycznym bootloaderem Zortraxa v1.0 i zgodną V9:** [pobierz ZIP instalacyjny v1.0 → v1.3](../SD_INSTALLATION/02_FACTORY_ZORTRAX_v1.0_to_v1.3/Inventure_boot_v1.3_SD_FABRYCZNA_V9_JEDNA_KARTA.zip) — SHA-256 `69e1c943284dd23d1cff71b07c6d57dea67d8cdeecc6df69a9045638ec017319`.

**ZIP rozpakuj na komputerze.** Na kartę FAT32 kopiujesz **cztery pliki z wnętrza właściwego archiwum**, nie sam plik ZIP. Szczegółowa instrukcja obu wariantów, także po angielsku: [SD_INSTALLATION/README.md](../SD_INSTALLATION/README.md).

## Wybór paczki SD

| Co jest teraz w drukarce? | Instalator na karcie | Pozostałe pliki |
| --- | --- | --- |
| Nasz **Inventure boot v1.2** | `INVENTUR.IVB` | `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN` |
| Oryginalny **Zortrax bootloader v1.0** na zgodnej V9 | `InventureUpdate.bin` | `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN` |

Sformatuj kartę jako **FAT32** i skopiuj cztery pliki **jednej wybranej paczki** do katalogu głównego. Nie mieszaj wersji. Pliki `ZBACKUP.BIN` i `ZBACK2.BIN` są na początku tylko **przygotowanymi miejscami na kopie**; nie są prawdziwymi backupami, dopóki drukarka ich nie zapisze i nie zweryfikuje.

Aplikacja instalacyjna zastępuje tymczasowo oryginalny program w obszarze `0x08010000`. `RESTORE.BIN` to obraz oryginalnej aplikacji Zortrax Inventure **1.6.1/r0323**, używany w naszych próbach; przed użyciem na innym egzemplarzu upewnij się, że jest właściwy. Firmware producenta podlega odrębnym prawom.

## A. Upgrade z Inventure boot v1.2 do v1.3

1. Sprawdź `INFO` oraz oznaczenie V9. Zachowaj niezależne kopie ustawień i Flash oraz możliwość odzyskania przez ST-Link; zapewnij stabilne zasilanie.
2. Włóż kartę wariantu A. Przerwij trzysekundowy autostart dowolnym przyciskiem.
3. W menu wybierz **Firmware on SD → Check SD package**. Po poprawnej weryfikacji wybierz **Install firmware**. Zwolnij przyciski i potwierdź **OK + GÓRA przez 2 sekundy**. W tym kroku instalujesz **tymczasową aplikację r9893**, a nie sektory bootloadera.
4. Wybierz **Start application / Launch application**, potwierdzając przytrzymaniem **OK + DÓŁ**, albo uruchom aplikację przy resecie. Zobaczysz **SD BOOT INSTALLER r9893**.
5. Wybierz **Backup current boot x2**. Poczekaj na poprawny zapis **i odczytową weryfikację obu kopii**. Jeśli pojawia się błąd, przerwij.
6. Wybierz **Install new boot**. Program ponownie sprawdzi oba backupy i zgodność starego bootloadera. Pierwsze potwierdzenie: naciśnij OK i puść; drugie: przytrzymaj **OK + GÓRA przez 5 sekund**. DÓŁ anuluje. **To etap kasowania sektorów 0–1**; nie przerywaj zasilania.
7. Po resecie zatrzymaj autostart v1.3 dowolnym przyciskiem. **W pamięci nadal znajduje się instalator r9893**, a nie program Zortraxa.
8. Wybierz **Firmware on SD → Choose firmware file → RESTORE.BIN → Check selected file → Install selected file**; potwierdź **OK + GÓRA przez 2 sekundy**. Nie instaluj ponownie pozostawionego na karcie pakietu serwisowego.
9. Wykonaj `VERIFY`, sprawdź oczekiwaną aplikację, wybierz `BOOT` lub zrestartuj drukarkę i pozwól na 3-sekundowy autostart. Powinno uruchomić się normalne menu Zortraxa.

## B. Fabryczny bootloader Zortraxa v1.0 → v1.3

1. Potwierdź zgodną płytę V9. Znany oryginalny obraz pierwszych 32 KiB Flash ma SHA-256: `19640ae302d918a79a243dbc7a5efcf055f78a1b459af4b50f3e66575af81752`. **Nie obchodź odmowy instalatora dla innego obrazu.**
2. Skopiuj z paczki B na FAT32: `InventureUpdate.bin`, `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN`.
3. Po włożeniu karty i uruchomieniu drukarki oryginalny mechanizm aktualizacji instaluje zaszyfrowaną aplikację serwisową r9893 w obszarze aplikacji `0x08010000`. Nie nadpisuje jeszcze fabrycznego bootloadera.
4. Gdy działa **SD BOOT INSTALLER r9893**, wykonaj **kroki A5–A9**: dwa sprawdzone backupy, świadome potwierdzenie zmiany sektorów 0–1, wybór `RESTORE.BIN`, `VERIFY`, uruchomienie fabrycznej aplikacji.

## Mapa pamięci i ograniczenia

| Flash STM32 | Funkcja |
| --- | --- |
| `0x08000000–0x08007FFF` — sektory 0–1 | Bootloader |
| `0x08008000–0x0800FFFF` — sektory 2–3 | Fabryczne NVM i kalibracja |
| `0x08010000–0x0803FFFF` — sektory 4–5 | Aplikacja / metadane |

Nigdy nie wybieraj **Mass Erase** ani zmiany zabezpieczeń RDP/OTP/Option Bytes bez osobnej procedury. Nie wyłączaj zasilania podczas zapisu sektorów bootloadera. Dwa pliki na jednej karcie nie zastępują niezależnego backupu. Jeśli rozruch zostanie uszkodzony, konieczny może być ST-Link/SWD.

Po instalacji sprawdź na OLED i przez UART `INFO`, `VERIFY`, `SDCHECK`, `RESETINFO` oraz pozycję **Back** w menu. Poprawna aplikacja ma uruchamiać się automatycznie po 3 sekundach bez naciskania klawiszy.

Szczegółowe funkcje i konsola: [FUNKCJE_I_KONSOLA_PL.md](FUNKCJE_I_KONSOLA_PL.md).
