# Audyt i uporządkowanie repozytorium Inventure boot — 29.10.2026

**Baza:** `682dcdce241573f66e0cadbce8a933b610febb38`. **Wydanie bieżące:** v1.5 / RELEASE 1.5-HW2. **Wynik kontroli repozytorium: PASS.**

## Co zbadano

Odczytano wszystkie 55 plików opublikowanego drzewa i porównano ich Git blob SHA z przypiętym commitem. Sprawdzono dokumentację, ilustracje, publiczne skrypty, archiwa i metadane wydania. Oddzielnie porównano opis menu/Hardware/instalatora z zachowanymi źródłami HW2, bez ich publikowania.

## Wykryte problemy i naprawa

| Problem | Naprawa |
|---|---|
| Siedem pełnych instrukcji 1.4 leżało bezpośrednio w docs obok 1.5 | Przeniesione do docs/v1.4, z oznaczeniem archiwum; bez przepisywania historii jako 1.5 |
| Ilustracje były oddzielone od katalogów opisów | Każda wersja ma własny images; wszystkie obrazy przeniesione bajtowo bez zmian |
| Skrócone mieszane PL/EN opisy 1.5 nie zastępowały kompletnych przewodników 1.4 | Pełne, osobne PL/EN funkcje/konsola i przykłady APP dla 1.5; dotychczasowe wejścia są jednoznacznymi indeksami językowymi |
| Historyczny SD_INSTALLATION sugerował bieżący sposób instalacji | Oznaczony jako archiwum v1.3; pełen dawny opis zachowany w docs/v1.3 |
| Opis pomocy ibtool.py wymieniał tylko 1.4 | Zmieniono wyłącznie docstring na 1.4/1.5; porównanie AST potwierdza niezmienność wykonywalnej logiki |
| Odnośniki manifestu i instrukcji wskazywały niezweryfikowany kontekst wersji | Przeliczone ścieżki, indeks docs, aktualny README i linki opisu Release |

## Bieżący, potwierdzony stan Hardware

Właściciel potwierdził instalację HW2 na jednej drukarce oraz poprawne odczyty rzeczywistych danych w Hardware **stałego bootloadera**. Nie jest to tylko symulacja. Ekran pokazuje Model, Hardware version, Serial number i **Print time**, nie całkowity czas zasilania. Dane ilustracyjne pozostają syntetyczne. Historyczny banner instalatora HW UNTESTED nie został zmieniony w przetestowanym binarium; jego znaczenie wyjaśnia instrukcja.

## Rzeczywiście wykonane kontrole tego audytu

| Zakres | Wynik |
|---|---:|
| Pełne pliki bazowego repozytorium | 55 |
| Instrukcje 1.4 przeniesione do archiwum | 7 |
| Przeniesione obrazy, identyczne bajtowo | 26 |
| Kontrola CRC archiwów ZIP | 6 |
| Zachowane binaria/pakiety i pliki sum | 10 |
| Asercje kontroli plików i narzędzi | 114 |

Kontrole narzędzi obejmują pack/inspect, odmowę złych danych i wektorów, rzeczywisty IVB instalatora, identyczność osadzonego BOOT, RESTORE, metadane zaszyfrowanego kontenera, opakowanie już odszyfrowanej APP oraz ramki UART na **modelu portu**, bez połączenia z drukarką. Szczegóły i liczbę odnośników podaje [AUDIT_CHECKS.json](AUDIT_CHECKS.json).

**Nie przeprowadzano nowej kompilacji firmware, pełnej regresji 3070/250 ani nowych prób fizycznych.** Te liczby w manifeście opisują zachowane wyniki wcześniejszego wydania HW2. Audyt publikacji nie zastępuje testów każdej płyty, prędkości, zaniku zasilania ani bezpieczeństwa alternatywnej APP. Zewnętrznych stron producentów nie audytowano; sprawdzono lokalne linki/sekcje i zasoby GitHub.

## Nowa struktura

```text
README.md                  aktualne wydanie i trzy pliki
 docs/README.md            wybór wersji
 docs/v1.5/                pełna aktualna dokumentacja, obrazy i audyt
 docs/v1.4/                archiwum P4-PERSIST-r2 i jego obrazy
 docs/v1.3/                zachowana starsza instrukcja
 firmware/v1.5/            niezmienione HW2: UPGRADE, FROM FACTORY, ST-Link
 firmware/v1.4/            niezmienione trzy pliki 1.4
 SD_INSTALLATION/          historyczne binaria 1.3, oznaczone jako archiwum
 tools/                    dwa publiczne skrypty i ich wspólny opis
```

Nie zmieniono release assets ani taga v1.5. Nowa dokumentacja jest na main; tag zachowuje oryginalny snapshot wydania. Archiwum 1.4 nie jest obietnicą możliwości downgrade z HW2. Nie opublikowano prywatnych źródeł, osobnych plików czcionek, sekretów, ELF/map ani danych egzemplarza. Brak nowego pliku licencji nie został zastąpiony domyślną deklaracją open-source.

[Dokumentacja 1.5](README.md) · [Archiwum 1.4](../v1.4/README.md) · [Wszystkie wersje](../README.md)
