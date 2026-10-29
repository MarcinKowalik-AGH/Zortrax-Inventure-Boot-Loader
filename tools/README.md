# Publiczne narzędzia hosta / Public host tools — Inventure v1.5

Wspólny format IVB dla opublikowanych bootloaderów v1.4 i v1.5-HW2. To narzędzia komputera, nie programy instalujące sam BOOT i nie źródła bootloadera.

| Plik | Zakres / Scope |
|---|---|
| [ibtool.py](ibtool.py) | `pack`, `inspect`, `serial`; pakowanie i kontrola IVB, transmisja IBD1 do już działającego własnego BOOT |
| [vendor_tool.py](vendor_tool.py) | Kontrola znanych, już odszyfrowanych aplikacji według SHA-256, opakowanie IVB; dla zaszyfrowanego ZRTX wyłącznie zewnętrzne metadane |

Python 3.9 lub nowszy. `pack`, `inspect` i kontrola vendor używają biblioteki standardowej; tylko transmisja `serial` wymaga `pyserial`. Uruchamiaj z katalogu głównego repozytorium; pobierz oba skrypty do tego samego folderu `tools`.

```sh
python3 tools/ibtool.py --help
python3 tools/vendor_tool.py --help
python3 -m pip install pyserial
```

**[Pełne przykłady PL dla 1.5](../docs/v1.5/KONSOLA_P4_PRZYKLADY_PL.md)** · **[Full v1.5 English examples](../docs/v1.5/P4_UART_EXAMPLES_EN.md)**

Nie ma kluczy odszyfrowywania/podpisywania ani syntezy tail20. Zaszyfrowany oryginalny pakiet instaluje się przez SD, nie konwertuje publicznym skryptem. Surowa APP zapakowana jako IVB nie jest rekonstrukcją pełnego payloadu producenta. Programy nie zmieniają ochrony pamięci ani nie zastępują testów peryferiów własnej APP.

Output files use exclusive creation: an existing output is refused, not overwritten. Close miniterm before using the sender; physical OK+UP confirmation remains required for `--update`. A successful `inspect` is not proof of safe Klipper operation.
