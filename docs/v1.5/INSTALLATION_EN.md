# Inventure boot v1.5-HW2 — installation manual

**Release:** v1.5 · **Build:** RELEASE 1.5-HW2 · **Published:** 29 October 2026  
**Target:** Zortrax Inventure V9 / STM32F207 / 256 KiB Flash. Author: Marcin Kowalik.

[Project](../../README.md) · [Polski](INSTALACJA_PL.md) · [Features/P4](FEATURES_AND_CONSOLE_EN.md) · [Manifest](RELEASE_MANIFEST.md) · [Archived v1.4 manual](../v1.4/INSTALLATION_EN.md)

The owner reported successful installation and operation on **one printer**. These are the exact tested binaries, not a new build. The report does not separately identify tests of all three installation routes. The installer still contains its build-time `V1.5 HW2 - HW UNTESTED` banner; the later hardware report is recorded here rather than modifying tested bytes.

**Hardware — physically confirmed:** on 29 October 2026 the owner explicitly confirmed that the permanent bootloader Hardware screen **correctly reads the actual printer data** on his device. This is an on-device confirmation, not just a model test. Manual previews still use clearly synthetic examples rather than private printer data.

## Navigation

[FROM FACTORY](#factory) · [UPGRADE](#upgrade) · [Shared SD/RESTORE stage](#installer) · [ST-Link](#stlink) · [Console](FEATURES_AND_CONSOLE_EN.md) · [APP examples](P4_UART_EXAMPLES_EN.md)

## 1. Select the correct route

| Current printer state | Download | Procedure |
|---|---|---|
| Recognized custom Inventure BOOT, including published v1.4 | [SD UPGRADE](../../firmware/v1.5/Inventure_boot_v1.5_HW2_STOCK_FONT_2026-10-29_SD_UPGRADE.zip) | B, then C |
| Exact recognized original V9 BOOT; write prerequisites verified | [FROM FACTORY / SD_FACTORY_V9](../../firmware/v1.5/Inventure_boot_v1.5_HW2_STOCK_FONT_2026-10-29_SD_FACTORY_V9.zip) | A, then C |
| Working direct SWD read/write access | [ST-Link 32-KiB BIN](../../firmware/v1.5/Inventure_boot_v1.5_HW2_STOCK_FONT_2026-10-29_STLINK_32KiB_0x08000000.bin) | D |

Do not use packages for M300/M200/Plus/Dual. Earlier LARGE_FONT and UI-MEM1 packages are not this HW2 release. Text version labels alone do not establish image compatibility.

## 2. Prerequisites, backups and memory boundaries

Save verified backups of **your actual printer**, not just a downloaded manufacturer application. The full 256-KiB Flash snapshot contains BOOT, NVM and APP; save OTP/UID/option-byte reads separately. Keep unique printer data private and store copies on another medium.

Before either SD route verify the V9 target, **RDP Level 0**, writable **BOOT sectors 0–1** and **APP sectors 4–5**, a suitable stock RESTORE image and stable power. The known original V9 BOOT is 32768 bytes, SHA-256 `19640ae302d918a79a243dbc7a5efcf055f78a1b459af4b50f3e66575af81752`. Previous custom BOOT images must match the installer's supported identities; only recognized immutable prefixes permit variable P4 journal bytes.

**No Mass Erase, Read Unprotect, `-rdu`, or option-byte changes to bypass a refusal.** The factory route first replaces APP with the installer; a later BOOT-write refusal does not restore APP automatically. Power loss during BOOT replacement may require SWD recovery. Backups are not an automatic A/B boot bank.

| Region | Addresses | SD BOOT installation | ST-Link route D |
|---|---|---|---|
| BOOT, sectors 0–1 | `0x08000000–0x08007FFF` | Replaced by installer | Replaced directly |
| P4 journal inside BOOT | `0x08007F00–0x08007FFF` | Reset to 250000 default | Reset |
| NVM, sectors 2–3 | `0x08008000–0x0800FFFF` | Preserved | Preserved; compare readback |
| APP/metadata, sectors 4–5 | `0x08010000–0x0803FFFF` | Temporary installer, then restore APP | Preserved; compare readback |

## 3. Verify files and prepare SD

Download [SHA256SUMS.txt](../../firmware/v1.5/SHA256SUMS.txt). Compare the complete SHA-256 using `shasum -a 256 FILE` on macOS, `sha256sum FILE` on Linux, or `Get-FileHash -Algorithm SHA256 FILE` in PowerShell. Stop if it differs.

Extract **one** SD ZIP on the computer. Copy its four files to **FAT32 SD root**:

| UPGRADE card | FROM FACTORY card | Purpose |
|---|---|---|
| `INVENTUR.IVB` | `InventureUpdate.bin` | Route-specific installer APP |
| `RESTORE.BIN` | `RESTORE.BIN` | Fixed stock APP 1.6.1/r0323 |
| `ZBACKUP.BIN` | `ZBACKUP.BIN` | First preallocated 32768-byte BOOT backup slot |
| `ZBACK2.BIN` | `ZBACK2.BIN` | Second preallocated 32768-byte BOOT backup slot |

The two A5-filled slots are **templates, not completed backups**. Never overwrite real backups with templates: first preserve them elsewhere and use a separately prepared card. Do not copy an unopened ZIP, private source archive, or standalone ST-Link BIN onto the installation card. Do not mix both installers. Safely eject the card.

<a id="factory"></a>

## 4. A — FROM FACTORY — original Zortrax BOOT

1. Complete prerequisites and backups **before inserting the card**, including protection-state checks.
2. Power down and insert the **SD_FACTORY_V9** card containing `InventureUpdate.bin`.
3. Power on. The compatible original BOOT processes the update and installs the service application. Do not interrupt this stage or remove the card.
4. Wait for **`SD BOOT INSTALLER - V9`**. The `Inventure boot v1.5` header shown by this temporary APP **does not mean that BOOT has already been replaced**.
5. Continue with C: two verified backups, separate physical confirmation, BOOT write/restart and APP restore.

![HW2 installer menu](images/10_installer_menu.png)

This is a native UI render, not a photograph or evidence of a separate factory-route hardware test. If the original screen remains or an error is reported, stop and check package/card/target conditions; do not assume success or change protection to force installation.

<a id="upgrade"></a>

## 5. B — UPGRADE — existing custom Inventure boot

1. Prepare the **SD_UPGRADE** card as in section 3.
2. Restart and interrupt the **5-second** autoboot countdown using a button. The custom BOOT does not install an SD file automatically.
3. In v1.3/v1.4/v1.5 choose `Firmware on SD → Choose firmware file → INVENTUR.IVB → Check selected file`.
4. After a successful check choose `Install selected file`. **Release all buttons**, then hold **OK+UP for 2 seconds when asked**. DOWN alone cancels. This writes the temporary installer into APP, **not BOOT yet**.
5. Choose `Start application → Launch application`; release buttons, then hold **OK+DOWN for 2 seconds**. UP alone cancels.
6. When the installer menu appears, continue with C.

![File list](images/05_files.png)
![Separate check/install actions](images/06_file.png)

Screens are from the new HW2 renderer; your older BOOT may look different. For v1.2 without file browsing, use `Check SD package` and `Install firmware` with one valid standard-name `INVENTUR.IVB`; the launch entry may be called `Start firmware`. UART equivalents are `SDCHECK`, `SDUPDATE`, then `BOOT`, with the same physical confirmations. A numeric selection must always come from the current `LIST`.

<a id="installer"></a>

## 6. C — Both SD routes — replace BOOT, then restore APP

### C1. Back up BOOT twice

Choose **`Backup current boot x2`**. Wait for both write/readback checks and RESTORE verification. Success is reported as **`TWO SD COPIES VERIFIED` / `SELECT INSTALL SEPARATELY`**, or **`TWO BOOT BACKUPS VERIFIED`** when the existing slots already match.

![Backup and verification](images/12_installer_backup.png)

An unrelated older backup is not silently overwritten. Opening `Hardware` or seeing the board-check result is not a substitute for two verified backups.

### C2. Confirm the separate BOOT replacement

Choose **`Install / reinstall boot`**. Wait during source/backup/RESTORE/write-prerequisite checks. Then follow the actual prompt:

1. Release all buttons.
2. Press **OK alone once, then release it**. DOWN cancels.
3. At the second prompt hold **OK+UP for five full seconds**. DOWN cancels. Do not hold the combination from the beginning of verification; selecting the menu entry is not this confirmation.
4. After acceptance the installer checks prerequisites again and writes BOOT. **Keep power and SD connected**. Buttons may be released after the gesture has been accepted.

![BOOT confirmation](images/13_installer_gesture.png)

Progress percentages refer to the named current phase. `--` may be shown when a reliable range is unavailable; it is not a fault or a fabricated completion percentage.

### C3. Restart and restore APP — required

On success the installer shows `NEW BOOT INSTALLED` / `REBOOTING TO BOOT MENU` and resets. **Interrupt autoboot**: APP still contains the installer. Keep the card inserted.

![Installer success](images/14_installer_success.png)

In the new BOOT explicitly choose `RESTORE.BIN` through `Firmware on SD → Choose firmware file`. Run `Check selected file`, then `Install selected file` with **OK+UP 2 s**. Run `Diagnostics → Verify Flash`. Only after success launch the APP with **OK+DOWN 2 s**.

UART alternative: `LIST`, actual `SELECT n` for RESTORE, `SDCHECK`, `SDUPDATE`, `VERIFY`, `BOOT`. `RESTORE.BIN` is not an automatic filename and `SELECT RESTORE.BIN` is not a command.

The supplied RESTORE installs **stock Zortrax 1.6.1/r0323**, not an arbitrary previous application. Restoring a custom APP such as a V9-specific Klipper build is a separate checked choice. Preserve the completed BOOT backups on the computer.

<a id="stlink"></a>

## 7. D — ST-Link/SWD — BOOT only, APP remains installed

1. Connect with power off, using the verified SWD connector for your board: **SWDIO, SWCLK, common GND and target-voltage reference as required by the actual probe**, plus NRST only as documented. Do not guess pin order or feed probe supply into a powered printer.
2. In STM32CubeProgrammer select **ST-LINK / SWD**, connect to the properly powered target and halt the MCU. Verify MCU identity and **256 KiB Flash**. Read protection status without changing it. Stop on access refusal; no Read Unprotect/Mass Erase.
3. Read **`0x40000` bytes from `0x08000000` twice**, to different files. Compare all bytes or full SHA-256 and keep the matching backups. Save readable identity/OTP/option information separately. Check that retaining the current APP is appropriate.
4. Load the **32768-byte BOOT BIN** linked above. Program address **`0x08000000`** and erase **sectors 0 and 1 only**, never 2–5 or the whole chip. Program and verify.
5. **Before starting the MCU**, read the full 256 KiB into `after.bin`. The first 32768 bytes must equal the new BOOT BIN; every byte from offset `0x8000` to the end must equal the original `before.bin`.
6. Only after both comparisons pass, reset/run, stop autoboot and check `INFO`, Hardware and `Verify Flash`. APP was not replaced by the installer; **do not install RESTORE unnecessarily**.

Independent host-side comparison, not a programming script:

```python
from pathlib import Path
before = Path('before.bin').read_bytes()
after = Path('after.bin').read_bytes()
boot = Path('Inventure_boot_v1.5_HW2_STOCK_FONT_2026-10-29_STLINK_32KiB_0x08000000.bin').read_bytes()
if len(before) != 0x40000 or len(after) != 0x40000 or len(boot) != 0x8000:
    raise SystemExit('Wrong file size — do not start the printer')
if after[:0x8000] != boot:
    raise SystemExit('BOOT mismatch — do not start the printer')
if after[0x8000:] != before[0x8000:]:
    raise SystemExit('NVM/APP changed — stop')
print('PASS: BOOT matches; NVM and APP preserved')
```

Run these comparisons before changing baud or launching APP; subsequent legitimate operations may change the P4 journal or NVM. The standalone BOOT BIN is not an APP package for `SDUPDATE`.

## 8. P4 configuration and acceptance checks

Freshly written BOOT starts at **250000, 8N1**. Choose the desired rate in `Diagnostics → UART → P4 baud rate`: **19200 / 57600 / 115200 / 250000 / 500000**, then immediately adjust your terminal. Normal APP updates preserve the saved rate. **UP+DOWN during startup** temporarily forces 250000 without overwriting the stored setting. The installer always uses its own fixed 250000.

![UART menu](images/03_uart.png)
![Baud selection](images/04_baud.png)

`INFO` in the permanent BOOT should report **`BUILD RELEASE 1.5-HW2`**. `Diagnostics → Hardware` reads the actual printer and stays until a fresh OK press. `Print time` is recorded printing time, not total powered-on time. Compare device data, exercise both list boundaries and direction changes, and retain exact errors if anything fails.

## 9. Troubleshooting

| Symptom | Response |
|---|---|
| Installer starts again | APP still contains it; explicitly restore APP, VERIFY and BOOT |
| `UNRECOGNIZED BOOT IMAGE` | Stop; do not bypass identity checks |
| `HASH`, `CRC`, `FORMAT`, `VECTOR`, `CHANGED` | Check exact file, hash and media; never force the write |
| `CONFIRM`, `BUTTONS` | Release keys and perform the requested gesture only when prompted |
| `HARDWARE`, `FLASH` | Investigate hardware/write prerequisites without changing protection to bypass refusal |
| `AMBIGUOUS_FILES`, `NOTFOUND` | Correct FAT32 root set; explicit LIST/SELECT |
| `DONE ALREADY_INSTALLED` | Identical APP, write intentionally skipped |
| Hardware `Unavailable` | A field has no reliable record; do not invent or hard-code it |
| No INV> after BOOT | APP now owns UART and uses its own protocol |

Keeping v1.4 available **does not guarantee a downgrade path**: its older installer may not recognize HW2. All images in this manual are native renders with synthetic device data. The owner's successful test concerns one printer, not independent acceptance of every route or power-loss case.
