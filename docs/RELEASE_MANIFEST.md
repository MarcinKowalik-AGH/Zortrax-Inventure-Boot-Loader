# v1.4 P4-PERSIST-r2 — manifest publikacji / publication manifest

**Data / Date:** 2026-10-25  
**Autor / Author:** Marcin Kowalik · mkowalik@agh.edu.pl  
**Boot:** Inventure boot v1.4, BUILD P4-PERSIST-r2  
**Instalator / Installer:** r9898  
**Sprzęt / Target:** Inventure V9 / STM32F207 / 256 KiB main Flash.

## Trzy dystrybucje binarne / Three binary distributions

| Plik / File | B | SHA-256 | Git blob SHA-1 |
|---|---:|---|---|
| [Inventure_boot_v1.4_P4_PERSIST_r2_SD_UPGRADE.zip](../firmware/v1.4/Inventure_boot_v1.4_P4_PERSIST_r2_SD_UPGRADE.zip) | 137282 | `327da4da2c53c6ee49ccb45121b2b973b18c99c93952c2af051d0f4e071c956b` | `d5904c72202d2163cfafb56a289174e5cd8640f1` |
| [Inventure_boot_v1.4_P4_PERSIST_r2_SD_FACTORY_V9.zip](../firmware/v1.4/Inventure_boot_v1.4_P4_PERSIST_r2_SD_FACTORY_V9.zip) | 151323 | `050d6531ac875e599dbfe3e79acc99dfb350210dd2d624f2666e8d626c4577b1` | `4e586ff973e3750b5e1061748365f83bf6d4a50b` |
| [Inventure_boot_v1.4_P4_PERSIST_r2_FULL_32KiB_0x08000000.bin](../firmware/v1.4/Inventure_boot_v1.4_P4_PERSIST_r2_FULL_32KiB_0x08000000.bin) | 32768 | `9ffd140879b6946bed63928fba3ff7b38ff3db289710a2e0845eecbd9caf10ea` | `f2ef16dc500a3398e082a0a993e3222d45ba98b2` |

Oba ZIP zawierają wyłącznie cztery pliki binarne: właściwy instalator, RESTORE.BIN i dwa prealokowane miejsca na kopie BOOT. Nie zawierają źródeł, narzędzi, ELF, map, raportów wewnętrznych ani prywatnych zrzutów. Osobny BIN ma dokładnie 32768 B. Sumy dotyczą niezmienionych plików przekazanych właścicielowi przed jego potwierdzoną próbą.

Both ZIPs contain exactly four binary files: their respective installer, RESTORE.BIN and two preallocated BOOT backup slots. The standalone BIN is 32768 bytes. These are the unchanged binaries delivered before the owner's successful hardware report.

**BOOT SHA-256:** `9ffd140879b6946bed63928fba3ff7b38ff3db289710a2e0845eecbd9caf10ea`. Prefix 32512 B SHA-256: `f7162464e699aa17b3768a42cad5ec18708debf41b2c1183ea98e522bac73830`. The canonical final 256 bytes are FF; that region becomes the saved P4 journal. FULL uses 32508 B and ends at **0x08007EFC**, leaving 4 B before the journal at **0x08007F00–0x08007FFF**.

RESTORE.BIN is the fixed **Zortrax 1.6.1/r0323** application payload, **164864 B**, SHA-256 `1368bdbddad941a8f7c025715946662a34d3def442d0d3c00af4315b54c8ba17`. It is not a backup of an arbitrary user's previously installed application. Manufacturer firmware retains separate rights and licensing.

## Publiczne narzędzia konsoli P4 / Public P4 host utilities

Dodano **dwa skrypty hosta**; nie zmieniono żadnego z trzech opublikowanych obrazów firmware:

| Skrypt | SHA-256 | Zakres |
|---|---|---|
| [`tools/ibtool.py`](../tools/ibtool.py) | `d23c6d0f3dd097dabed548f5ba1f3b87f91d13fd7d28b2c3c294a377faabd254` | IVB pack/inspect/serial, transmisja IBD1 |
| [`tools/vendor_tool.py`](../tools/vendor_tool.py) | `0c03dd74b4e763cf68b96325150bf01d2110a808a427e34fe8a792370cb377a8` | Sprawdzenie SHA-256 ośmiu znanych, **już odszyfrowanych** APP, pakowanie IVB, inspekcja metadanych ZRTX |

Public tools include **no encryption/decryption keys, no HMAC signing key, no stored tail20 bytes, and no tail synthesis**. Encrypted ZRTX conversion to IVB is deliberately unavailable; install supported encrypted stock packages via the SD route. Already-decrypted raw stock wrapped as IVB is a **custom-manifest representation**, not exact vendor-tail restoration. Full pre-existing plaintext vendor payloads are accepted only by complete SHA-256 allowlist match. Host-tool checks were conducted offline; not separate flash hardware tests.

## Status sprzętowy / Hardware report

**25.10.2026, po dostarczeniu r2:** właściciel napisał: „ok wgrałem do drukarki i przetestowałem opcje działa bez problemu”. Odnosi się to do końcowej v1.4 **P4-PERSIST-r2**, z podmenu UART, oryginalnym fontem i trwałym zapisem P4. Od tej próby nie zmieniono binariów.

The owner's report confirms installation and operation of the tested r2 build. It does not enumerate a separate test of every baud rate, long-duration retention, electrical measurements, power-loss cases, or all three programming routes. Those detailed results are not invented here.

**History:** the earlier repository recorded successful physical v1.2→v1.3 SD upgrade and factory-Zortrax→v1.3 SD installation followed by stock application restore and boot. Those remain v1.3 results, not new claims that both r9898 routes were separately exercised during the latest r2 report.

## Walidacja programowa / Software validation

| Sprawdzenie / Check | Wynik / Result |
|---|---:|
| Bootloader native/model tests | 2395/2395 |
| Bootloader tests after clean-source extraction and rebuild | 2395/2395 |
| ARM bounds / SRAM / vectors / variant checks | 99/99 |
| r9898 installer tests | 157/157 |
| Installer tests after clean-source extraction and rebuild | 157/157 |
| Cross-version package/stock compatibility assertions | 1604/1604 |
| Native ASan/UBSan/bounds exercises | 4 × 20000 iterations, PASS |

All compared BOOT BIN/ELF variants and six installer artifacts rebuilt byte for byte. No failures, errors or skips remain in final pytest reports. These totals overlap in scope and are not added as independent hardware tests.

Font evidence: 120 original r0323 glyphs plus the project's custom bullet; exact widths and row pixels checked, including all 65536 BMP lookups. All 9 ring frames remain exact. Menu actions, both Back transitions, chevron direction, P4 storage and readback constraints were checked.

## Rozpoznawanie i warunki / Recognition and conditions

r9898 preserves nine historical complete BOOT hashes and recognizes exact immutable prefixes for released r1 and r2. Saved/torn P4 journal bytes are permitted only for those exact prefixes. Both backup files must still match all 32768 current bytes. Version text alone is insufficient; `UNRECOGNIZED BOOT IMAGE` must not be bypassed.

Factory BOOT reference: SHA-256 `19640ae302d918a79a243dbc7a5efcf055f78a1b459af4b50f3e66575af81752`. A matching factory BOOT is not the only condition: the installer also requires RDP0, writable sectors 0–1, the expected MCU/Flash environment, a suitable supply, the two exact backups and valid RESTORE. The complete SD route also requires writable APP sectors 4–5. Check these conditions before starting: the first stage replaces APP before r9898 checks permission to replace BOOT. The installer never changes option bytes or disables protection.

Every canonical BOOT installation resets the P4 journal to default **250000**. Normal application updates preserve it. The installer itself uses 250000, 8N1 regardless of a previously saved bootloader-console rate.

## Dokumentacja i ilustracje / Documentation and illustrations

The illustrated [Polish](INSTALACJA_PL.md) and [English](INSTALLATION_EN.md) manuals cover factory SD, custom-BOOT upgrade and ST-Link. OLED images are generated from the actual native C renderers. Installer status screens are captured from native backup/install/confirmation runs with a simulated SD/Flash backend; selected menu states are rendered using actual labels. They are not photographs or proof of new physical runs. r9898 uses its existing font; the new bootloader uses the original stock proportional font.

Publication originally added only the three binary distributions, checksums, manuals and PNG illustrations. A later documentation update also added two **secret-free host-side Python scripts**, without changing those binaries. No production source code, assembler, ELF, map, linker scripts, cryptographic analysis, unique printer dump, NVM, OTP, UID or option-byte snapshot is published. Existing historical v1.3 ZIPs remain unchanged.
