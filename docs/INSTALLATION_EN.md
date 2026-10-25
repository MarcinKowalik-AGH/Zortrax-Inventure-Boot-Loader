# Installing Inventure boot v1.4

**Build:** P4-PERSIST-r2 · **SD service installer:** r9898  
**Target:** the supported Zortrax Inventure V9 / STM32F207 / 256 KiB Flash  
**Author:** Marcin Kowalik · mkowalik@agh.edu.pl

[Polska instrukcja](INSTALACJA_PL.md) · [Downloads](../README.md) · [Release manifest](RELEASE_MANIFEST.md) · [Features and console](FEATURES_AND_CONSOLE_EN.md)

This manual covers three installation methods: the original factory bootloader, an existing Inventure boot v1.2/v1.3/v1.4, and direct ST-Link/SWD programming. Both SD methods temporarily replace the printer application with the r9898 service installer, back up and replace BOOT, and then require an explicit application restore. ST-Link writes BOOT directly and preserves the existing application when the procedure below is followed.

**Hardware feedback, 25 October 2026:** the project owner reported installing this final v1.4 build and testing its options successfully. The published binaries are unchanged after that report. Earlier physical tests covered both the v1.2→v1.3 SD upgrade and factory→v1.3 installation with application restore. The latest r2 report does not separately document a new test of all three programming methods, every baud rate or every failure scenario. See the [release manifest](RELEASE_MANIFEST.md) for the exact scope.

The illustrations below are generated from the actual UI code. Installer status frames come from native execution with a simulated SD/Flash backend; selected menu states use the real renderer and labels. They are not photographs or additional physical test results. The installer retains its older font; v1.4 uses the original proportional r0323 font. Screens from older installed bootloaders may look different.

## 1. Choose the correct download

| Current installation / method | Download | Intended use |
|---|---|---|
| Recognized Inventure boot v1.2, v1.3 or earlier v1.4 | [Inventure_boot_v1.4_P4_PERSIST_r2_SD_UPGRADE.zip](../firmware/v1.4/Inventure_boot_v1.4_P4_PERSIST_r2_SD_UPGRADE.zip) | Four files for the SD upgrade route |
| Recognized original Zortrax BOOT on a compatible V9 with the required Flash access | [Inventure_boot_v1.4_P4_PERSIST_r2_SD_FACTORY_V9.zip](../firmware/v1.4/Inventure_boot_v1.4_P4_PERSIST_r2_SD_FACTORY_V9.zip) | Four files for the factory SD route |
| ST-Link / SWD with readable Flash and writable BOOT sectors | [Inventure_boot_v1.4_P4_PERSIST_r2_FULL_32KiB_0x08000000.bin](../firmware/v1.4/Inventure_boot_v1.4_P4_PERSIST_r2_FULL_32KiB_0x08000000.bin) | Raw 32768-byte BOOT image at **0x08000000** |

Verify the downloaded file against [SHA256SUMS.txt](../firmware/v1.4/SHA256SUMS.txt) before use. The [manifest](RELEASE_MANIFEST.md) also lists file sizes and hashes. Each ZIP contains exactly four binary files; the ZIP itself is not the file that the printer installs.

**Do not rename the raw 32 KiB BOOT image to `INVENTUR.IVB` or `InventureUpdate.bin`.** These are different formats and installation stages.

## 2. Requirements before starting either SD route

Check these conditions **before allowing the first SD update to replace the application**:

- The board is the supported **Inventure V9**, with the expected **STM32F207 and 256 KiB Flash**. A different board or Flash size is outside this procedure.
- The existing BOOT is recognized by r9898. A displayed version number alone is insufficient: recognition checks the actual image. The reference original factory BOOT has SHA-256 `19640ae302d918a79a243dbc7a5efcf055f78a1b459af4b50f3e66575af81752`.
- **RDP is Level 0**, and write protection is disabled for **BOOT sectors 0/1 and application sectors 4/5**. For this STM32F2, RDP0 is the raw value `0xAA`; an nWRP bit of **1** means that sector is writable. Establish this from a verified service record or a read-only Option bytes inspection, such as the ST-Link procedure below. If access conditions are unknown, do not start the SD update.
- The printer is compatible with the supplied **Zortrax 1.6.1/r0323** application. `RESTORE.BIN` restores that fixed version, not an arbitrary application that happened to be installed previously.
- Power is stable and the FAT32 card is reliable and writable. Save any needed card contents first. Preserve available independent printer backups before modification.

The factory package is an entry route through a recognized factory bootloader. It does **not** remove read or write protection. The first SD stage writes the service application **before** r9898 checks permission to replace BOOT. If that later check rejects the operation, the service application may already occupy APP; rejection does not automatically restore the previous application.

Do not use mass erase, Read Unprotect / `-rdu`, RDP changes or other Option byte changes to bypass a rejection. On this STM32F2, changing RDP1 to RDP0 erases main Flash and backup SRAM, including the factory NVM stored in main Flash. A dump obtained by running firmware does not by itself prove that SWD access is unlocked. See [ST PM0059, sections 2.6.3–2.6.4](https://www.st.com/resource/en/programming_manual/pm0059-stm32f205215-stm32f207217-flash-programming-manual-stmicroelectronics.pdf).

| Address range | Contents | Treatment during installation |
|---|---|---|
| `0x08000000–0x08007FFF` | BOOT, sectors 0–1, 32 KiB | Replaced with v1.4 |
| `0x08008000–0x0800FFFF` | Factory NVM, sectors 2–3 | Preserved |
| `0x08010000–0x0803FFFF` | Application and metadata, sectors 4–5 | Replaced by r9898, then RESTORE on SD routes; preserved by BOOT-only ST-Link programming |

Replacing BOOT is not atomic across a power failure. Two SD copies preserve the old bytes but do not make an interrupted BOOT write bootable. SWD recovery may be needed if power is lost while BOOT is being erased or programmed.

## 3. Prepare one SD card

1. Download **one** ZIP from section 1, matching the current bootloader.
2. Extract it on the computer.
3. Prepare a writable **FAT32** card. Copy the four extracted files directly into its root directory, not inside a folder and not as an unopened ZIP.
4. Check the root contents against the appropriate row:

| Route | Service application package | Files used by the installer |
|---|---|---|
| Factory V9 | `InventureUpdate.bin` | `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN` |
| Existing Inventure boot | `INVENTUR.IVB` | `RESTORE.BIN`, `ZBACKUP.BIN`, `ZBACK2.BIN` |

5. Do not mix the two sets. Remove other update candidates, including an old `INVENTUR.BIN` or the other route's installer file. Safely eject the card from the computer.

`ZBACKUP.BIN` and `ZBACK2.BIN` are each **32768 bytes**. In the downloaded ZIP they contain preallocated `A5` placeholders. **They are not device backups yet.** The installer writes into those existing file extents and verifies both copies; it does not create or enlarge files.

After a successful backup, each file contains the entire current 32 KiB BOOT, including any saved P4 settings. They do not contain the whole Flash, factory NVM, OTP or complete printer configuration. Two files on the same card are not independent storage. Archive the real copies on the computer after installation. For a later installation, preserve those archived copies and use fresh placeholders from the ZIP; do not overwrite your only real backup with a template.

The shared `RESTORE.BIN` is **164864 bytes**, SHA-256 `1368bdbddad941a8f7c025715946662a34d3def442d0d3c00af4315b54c8ba17`, and contains the known **1.6.1/r0323** application. It must remain unchanged. Manufacturer firmware retains its separate rights and licensing.

### Panel controls and result screens

Use **UP/DOWN** to move and the centre **OK** button to select. Release buttons after selecting an operation. A held selection button is not a fresh confirmation.

| Operation | Confirmation after releasing all buttons |
|---|---|
| Install an application package | Hold **OK + UP for 2 seconds**; DOWN cancels |
| Manually launch the installed application | Hold **OK + DOWN for 2 seconds**; UP cancels |
| Replace BOOT in r9898 | Fresh press and release of **OK alone**, then hold **OK + UP for 5 seconds** |

In v1.4, operation result screens return to the menu automatically after **3 seconds**. Release the buttons and wait; pressing OK is not needed to dismiss them. The r9898 installer uses a shorter **1.8-second** result display. Select the next action with a new press after the menu returns.

## 4. Factory SD installation

Use this route only with the recognized original factory BOOT and the prerequisites in section 2.

1. With the printer powered off, insert the prepared **SD_FACTORY_V9** card containing `InventureUpdate.bin`, `RESTORE.BIN`, `ZBACKUP.BIN` and `ZBACK2.BIN`.
2. Power on the printer normally. **Do not hold a special button combination.** The supported factory bootloader checks the card during startup and installs the service application from `InventureUpdate.bin` into the application area at `0x08010000`.
3. Leave power and the card connected while the factory update runs. Known factory messages include `InventureUpdate.bin found.` and `Update done.`. These original factory screens are described here rather than reconstructed as if they were v1.4 screens.
4. After the update, the factory bootloader launches r9898 automatically. **No second manual reset is required.** The short introduction identifies `INVENTURE SD BOOT INSTALLER r9898`, followed by the menu `SD BOOT INSTALLER - V9`.
5. Continue with **section 6**, starting with `Backup current boot x2`, then complete **section 7** to restore the printer application. Reaching the service installer alone does not finish the installation.

If the expected service menu does not appear, stop and record the displayed message. Do not change filenames or switch to a different package to defeat a failed check.

## 5. SD upgrade from an existing Inventure boot

This route supports recognized existing v1.2, v1.3 and v1.4 images. The first stage installs an application package through the existing bootloader; it does not yet replace BOOT.

### Main route, including v1.2

1. With the printer powered off, insert the prepared **SD_UPGRADE** card containing `INVENTUR.IVB`, `RESTORE.BIN`, `ZBACKUP.BIN` and `ZBACK2.BIN`.
2. Power on and press any panel button during the existing bootloader's countdown, if shown, to enter its menu. Release the button. Older versions may have a different countdown duration from v1.4.
3. Open **Firmware on SD → Check SD package**. On a fresh startup with this four-file card, the automatic package candidate is `INVENTUR.IVB`; `RESTORE.BIN` is not an automatic candidate. Wait for a successful result and for the menu to return.
4. Select **Firmware on SD → Install firmware**. Release all buttons when prompted, then hold **OK + UP for 2 seconds**. Do not remove power or the card during the write. This writes the **r9898 service application** to APP; the existing BOOT is still in place.
5. After success, release the buttons and wait for the menu. Select **Back** to return to the main menu. In original v1.2/v1.3 menus, Back is at the end of the submenu, so scroll if necessary.
6. Select **Start application → Launch application**. In **v1.2**, the main-menu entry is named **Start firmware**; its submenu is still titled `Start application`, with `Launch application` inside it.
7. Release all buttons, then hold **OK + DOWN for 2 seconds**. The service application starts immediately after this confirmation. Its introduction identifies **r9898**, followed by `SD BOOT INSTALLER - V9`.
8. Continue with **section 6**, then complete the application restore in **section 7**.

![Main SD upgrade route: Check SD package and Install firmware](images/v1.4/upgrade-00-auto.png)

*These examples use the v1.4 renderer. Earlier installed versions can use a different font and menu layout; the main route above also works without a file browser.*

### Optional explicit file selection on versions with a browser

If the installed bootloader offers **Choose firmware file**, you may replace steps 3–4 above with **Firmware on SD → Choose firmware file → INVENTUR.IVB**, followed by **Check selected file** and then **Install selected file**. Confirm the installation with a fresh release and **OK + UP for 2 seconds**. Then return to the main menu and launch r9898 as in steps 6–7.

![Optional browser route: select INVENTUR.IVB and check the selected file](images/v1.4/upgrade-01-select.png)

![Optional browser route: confirm the service application write](images/v1.4/upgrade-02-install.png)

The original v1.2 has no file browser, so this optional route is not required for v1.2. An explicit file selection remains active until reset or a console `SELECT AUTO`; use the page titled `INVENTUR.IVB` when following this option. Later, select `RESTORE.BIN` explicitly for the restore.

## 6. Common r9898 procedure: back up and replace BOOT

Both SD routes now use the same installer. Its menu contains:

| Menu item | Purpose |
|---|---|
| `Backup current boot x2` | Write and verify both complete current-BOOT copies |
| `Install / reinstall boot` | Separately confirm and replace BOOT |
| `Info / Diagnostics` | Show installer information and compatibility diagnostics |
| `Restart` | Restart the controller |

The installer uses **P4 at 250000 baud, 8N1**, even when the previous bootloader had a different saved console rate. A terminal is not required for the panel procedure.

1. Select **Backup current boot x2**. Wait while the display shows `BACKUP CURRENT BOOT x2` / `KEEP POWER ON`.
2. Require a successful result: **`TWO SD COPIES VERIFIED` / `SELECT INSTALL SEPARATELY`**. If both slots already contained the exact current BOOT, the result may instead be `TWO BOOT BACKUPS VERIFIED` / `READY FOR BOOT INSTALL`. Wait approximately 1.8 seconds for the menu.
3. Select **Install / reinstall boot** as a separate action. The backup command does not install automatically. The installer checks the two complete matching copies, RESTORE, the recognized BOOT, hardware and write conditions.
4. At **`TWO BOOT BACKUPS VERIFIED` / `PRESS OK ONCE / DOWN CANCEL`**, release all buttons. Make a **fresh press and release of OK alone**. The OK press used to select the menu item does not count.
5. At **`ERASE BOOT SECTORS 0/1` / `HOLD OK+UP 5 SEC`**, hold **OK + UP continuously for 5 seconds**. Releasing early restarts the hold time; DOWN cancels.
6. During **`INSTALLING NEW BOOT` / `DO NOT REMOVE POWER`**, keep power and the card connected. Do not press additional controls or reset the printer. BOOT sectors 0/1 are being replaced and checked.
7. Success shows **`NEW BOOT INSTALLED` / `REBOOTING TO BOOT MENU`**. After about one second the controller resets into the new bootloader.
8. **Press any button during the new 5-second countdown, then release it.** The application is still r9898 at this point. Continue immediately with the restore in section 7.

![Installer: back up the current BOOT twice and verify both copies](images/v1.4/sd-01-backup.png)

![Installer: separate selection, fresh OK confirmation and five-second OK plus UP hold](images/v1.4/sd-02-confirm.png)

![Installer completion and the new bootloader countdown to interrupt](images/v1.4/sd-03-restart.png)

If you miss the countdown, r9898 starts again. Choose **Restart** in the installer and interrupt the next bootloader countdown. **Do not repeat Install / reinstall boot merely because the service menu reappeared.** Starting the installer does not automatically replace BOOT again.

A panel rejection may show `OPERATION REJECTED` / `HARDWARE`. This is a combined error category: protection, an unknown BOOT, an incompatible MCU/Flash environment or a supply check may be responsible. It does not identify RDP by itself. Stop and retain the diagnostic message; do not bypass checks. If BOOT programming itself fails, `BOOT INSTALL FAILED` / `SWD MAY BE REQUIRED` may appear before the generic error handler returns to an error/menu screen. Do not assume the old BOOT remains intact after a write failure.

## 7. Restore the Zortrax application and finish the SD installation

This part takes place in the **new v1.4 bootloader**, after interrupting its countdown. The service application still occupies APP until the following restore succeeds.

1. Open **Firmware on SD → Choose firmware file**.
2. On **Files - select, then verify**, select **RESTORE.BIN**. File order can vary on a real FAT card. Confirm that the selected-file page title is `RESTORE.BIN`; do not select `INVENTUR.IVB` or `InventureUpdate.bin` again.
3. Choose **Check selected file**. Selecting a filename alone does not verify it. Wait for **`OPERATION COMPLETE` / `OK`**, release the buttons and allow the 3-second result screen to return automatically.
4. On the same `RESTORE.BIN` page, choose **Install selected file**. At **`CONFIRM WRITE` / `RELEASE BUTTONS`**, release all buttons. At **`HOLD OK + UP FOR 2 S` / `DOWN: CANCEL`**, hold **OK + UP for 2 seconds**.
5. Keep power and the card connected during the write and verification. Wait for **`OPERATION COMPLETE` / `OK`**, release the buttons and wait 3 seconds. If the application was already exactly identical, the verified result may be **`ALREADY INSTALLED` / `FLASH WRITE SKIPPED`**; it also returns automatically. A successful write does not launch the application automatically.

**Factory-card example** — the browser includes `InventureUpdate.bin`:

![Restore selection and confirmation using the factory SD card](images/v1.4/factory-04-restore.png)

**Upgrade-card example** — the browser includes `INVENTUR.IVB`:

![Restore selection and confirmation using the upgrade SD card](images/v1.4/sd-04-restore.png)

6. Return to the main menu by selecting **Back to files → Back → Back**: selected-file page → file list → Firmware on SD → main menu. Use a new OK press for each selection.
7. Open **Diagnostics → Verify Flash**. Require **`OPERATION COMPLETE` / `OK`**, then release and wait for the automatic return. Select **Back** to return to the main menu. This checks the installed application in Flash. `VERIFY` is the corresponding UART command, not the name of a main-menu item.
8. After successful verification and return to the menu, **power off**, remove the installation card, and copy the now-real **ZBACKUP.BIN** and **ZBACK2.BIN** to a dated folder on the computer. Keep both copies. The installation card is no longer required to boot the restored application.
9. Power on without that installation card. Leave the new **5-second countdown** uninterrupted to start the verified Zortrax application. Confirm that the normal printer interface loads.

For an immediate manual start instead of waiting for autoboot, interrupt the countdown and select **Start application → Launch application**. Release all buttons at **`START APP REQUEST` / `RELEASE BUTTONS`**, then hold **OK + DOWN for 2 seconds** when prompted. The handoff status is **`START APPLICATION` / `SWITCHING TO ZORTRAX`**. That status is generic; the successful RESTORE and Verify Flash steps establish which application is present.

![Manual application launch: release buttons, then hold OK plus DOWN](images/v1.4/sd-05-start.png)

The SD installation is complete after the restored **Zortrax 1.6.1/r0323** application starts successfully and the BOOT backups have been archived. Continue with section 9 to select and save the desired P4 console rate.

## 8. Direct installation with ST-Link / SWD

This method writes only the 32 KiB BOOT region. It does not run r9898 or replace the existing application. It requires working SWD access; it is not a protection-unlock procedure.

### 8.1 File, address and preserved regions

Use only **`Inventure_boot_v1.4_P4_PERSIST_r2_FULL_32KiB_0x08000000.bin`**.

| Parameter | Required value |
|---|---|
| File size | **32768 bytes / 0x8000** |
| Programming address | **0x08000000** |
| Sectors erased and written | **0 and 1 only**, `0x08000000–0x08007FFF` |
| NVM to preserve | `0x08008000–0x0800FFFF`, sectors 2–3 |
| Application and metadata to preserve | `0x08010000–0x0803FFFF`, sectors 4–5 |
| BOOT SHA-256 | `9ffd140879b6946bed63928fba3ff7b38ff3db289710a2e0845eecbd9caf10ea` |

Check the file size and SHA-256 **before erasing**. Neither `INVENTUR.IVB` nor `InventureUpdate.bin` from an SD package is the raw BOOT programming file.

### 8.2 Connect and halt the target

Install [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html). With power off, connect the corresponding **SWCLK, SWDIO, GND and NRST** signals, plus the probe's target-voltage reference **VTref/T_VCC** to the board's logic voltage. Use the printer's normal supply. VTref is a voltage reference; it is not an instruction to power the whole printer from the probe. Adapter pin numbers differ, so use the signal labels for your actual ST-Link. This manual does not assume an unverified P4 connector orientation or adapter pin numbering.

In CubeProgrammer select **ST-LINK → SWD**, **Connect under reset** and **Hardware reset**. Connect under reset requires NRST and catches the target at startup. Start at **1000 kHz**, or a lower supported frequency. Confirm the expected STM32F207 and 256 KiB Flash. Keep the core halted throughout programming and the final readback. See the [official ST-Link connection documentation](https://dev.st.com/stm32cube-docs/prog/2.23.0/en/docs/markup/STLink_Connection_page.html).

### 8.3 Inspect protection without changing it

Read **Option bytes**, but do not apply any changes. Continue only with **RDP Level 0** and **BOOT sectors 0/1 writable**. RDP0 is `0xAA`; nWRP=1 means that sector is unprotected. The GUI may display descriptive states instead of raw bits.

**Stop** if Flash cannot be read, RDP1/RDP2 is active or either required BOOT sector is protected. Do not use Read Unprotect, `-rdu`, RDP changes, `-ob NAME=VALUE`, mass erase or OTP programming. RDP1 blocks debugger Flash access, and regression from RDP1 to RDP0 mass-erases the main Flash and backup SRAM. A readable firmware-mediated dump does not establish SWD permission. See [ST PM0059](https://www.st.com/resource/en/programming_manual/pm0059-stm32f205215-stm32f207217-flash-programming-manual-stmicroelectronics.pdf).

The BOOT-only ST-Link write does not need to write sectors 4/5. If you later restore or replace an application, that separate operation also requires writable application sectors.

### 8.4 Read and save the complete BEFORE image

In **Memory & file edition / Device memory**, set address **0x08000000** and size **0x40000** (**262144 bytes**). Choose **Read**, then **Save As…** to save **BEFORE.bin** in a new folder. Check its exact size. Save the current Option bytes values locally, for example as a screenshot, without modifying them.

Do not erase if the full read fails, the length differs or the file is not a current snapshot of this printer. Preserve earlier backups separately. [CubeProgrammer memory read/export documentation](https://dev.st.com/stm32cube-docs/prog/2.23.0/en/docs/markup/CubeProg_UserManual/Memory_file_edition.html).

### 8.5 Erase only BOOT sectors 0 and 1

In **Erasing & programming**, select only:

- Sector **0**: start **0x08000000**, length **16 KiB**.
- Sector **1**: start **0x08004000**, length **16 KiB**.

Choose **Erase selected sectors** and require success. Do not select sectors 2–5 and do not use **Full chip erase**. Do not release the core to run or manually power-cycle the printer with BOOT erased; continue programming.

### 8.6 Program and verify the raw BOOT file

Select the verified 32768-byte file and set its start address to **0x08000000**. Set:

| Option | Setting |
|---|---|
| **Verify after programming** | **On** |
| **Skip flash memory erase before programming** | **On**, because the two required sectors were explicitly erased successfully |
| **Run after programming** | **Off** |

Choose **Start programming**. Require successful programming and verification. A failure is a reason to stop and inspect the result, not to expand the erase range. [CubeProgrammer erase/program documentation](https://dev.st.com/stm32cube-docs/prog/2.23.0/en/docs/markup/CubeProg_UserManual/Memory_programming_and_erasing.html).

### 8.7 Full AFTER readback before execution

While the core remains halted, read **0x40000 bytes from 0x08000000** again and save **AFTER.bin**. Before running the printer, verify both conditions:

1. The first **32768 bytes** of AFTER.bin exactly equal the downloaded BOOT file.
2. Every remaining byte, offsets **0x8000–0x3FFFF** (**229376 bytes**), is identical in BEFORE.bin and AFTER.bin.

The second comparison covers all NVM and application bytes. Use the immediately preceding BEFORE snapshot, not an unrelated older dump: normal application use can change NVM. Perform this strict check before starting the application or saving a P4 setting, which can legitimately change the respective stored regions later.

The following Python 3 snippet reads three local files from the current directory. It performs no device access and writes nothing. Place the named files together, run the snippet with Python 3, and require every line to report **PASS**:

```python
from pathlib import Path
import hashlib

before = Path("BEFORE.bin").read_bytes()
after = Path("AFTER.bin").read_bytes()
boot = Path("Inventure_boot_v1.4_P4_PERSIST_r2_FULL_32KiB_0x08000000.bin").read_bytes()
expected = "9ffd140879b6946bed63928fba3ff7b38ff3db289710a2e0845eecbd9caf10ea"

checks = {
    "BEFORE: 262144 bytes": len(before) == 262144,
    "AFTER: 262144 bytes": len(after) == 262144,
    "BOOT: 32768 bytes": len(boot) == 32768,
    "BOOT SHA-256": hashlib.sha256(boot).hexdigest() == expected,
    "Exact BOOT readback": after[:32768] == boot,
    "NVM and application unchanged": after[32768:] == before[32768:],
}
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL"), name)
if not all(checks.values()):
    raise SystemExit("STOP: the readback does not match.")
print("PASS: BOOT programmed; NVM and application preserved.")
```

If any condition fails, do not start the application. Keep both dumps and the programming log for analysis. Do not try to repair a mismatch by mass-erasing the device.

### 8.8 Disconnect and check the first boot

After all comparisons pass, disconnect the programmer session, power off and remove the programming leads. Power on and interrupt the 5-second countdown with a panel button. Confirm v1.4 in **About**. If using the console, `INFO` identifies **`BUILD P4-PERSIST-r2`**.

The existing application was preserved, so a BOOT-only ST-Link update does not by itself require RESTORE. If APP already contains the service installer or an invalid image, write the appropriate application separately through the new bootloader; section 7 describes the supplied r0323 restore. Replacing BOOT alone does not repair APP.

The new image starts with **250000 baud, 8N1**. Select the desired persistent rate as described in section 9.

### 8.9 Optional CLI equivalents

These examples use the officially documented STM32CubeProgrammer 2.23.0 CLI syntax. They assume `STM32_Programmer_CLI` is in PATH and that you are working in a new folder. On Windows, use `STM32_Programmer_CLI.exe`. On macOS, substitute the actual executable path if needed: Intel packages use `STM32CubeProgrammer.app/Contents/MacOs/bin/`, and Apple Silicon packages use `Contents/Resources/bin/`.

First read protection and the full current Flash:

```sh
STM32_Programmer_CLI -c port=SWD mode=UR reset=HWrst freq=1000 -ob displ
STM32_Programmer_CLI -c port=SWD mode=UR reset=HWrst freq=1000 -u 0x08000000 0x40000 BEFORE.bin
```

Inspect the reported RDP/WRP state, check BEFORE.bin and verify the source BIN's size/hash. Only then execute the following commands **one at a time**, continuing only after success:

```sh
STM32_Programmer_CLI -c port=SWD mode=UR reset=HWrst freq=1000 -e 0 1
STM32_Programmer_CLI -c port=SWD mode=UR reset=HWrst freq=1000 -skiperase -w "Inventure_boot_v1.4_P4_PERSIST_r2_FULL_32KiB_0x08000000.bin" 0x08000000 -v -u 0x08000000 0x40000 AFTER.bin
```

Do not add `-rst`, `-g` or `-s` before the AFTER comparison. `-v` must immediately follow the `-w` file/address arguments. `-e 0 1` selects precisely the two BOOT sectors; `-skiperase` prevents a second implicit erase during the write. Use the same full comparison from section 8.7 before starting the printer. These are documentation-verified examples, not a claim that these commands were executed on hardware while preparing this manual. [Official CLI reference](https://dev.st.com/stm32cube-docs/prog/2.23.0/en/docs/markup/CubeProg_Command_Lines.html).

## 9. Save the P4 console rate after installation

Every installation of the canonical BOOT image resets its settings journal and starts at **250000 baud, 8N1**. This includes SD installation, reinstallation and the full 32 KiB ST-Link write. A previous saved baud value is retained in the old BOOT backups, but is not automatically migrated into the new image.

1. Enter the bootloader menu and open **Diagnostics → UART**. UART appears immediately after **Display test**.
2. Choose **P4 baud rate**.
3. Select **19200, 57600, 115200, 250000 or 500000** with OK.
4. If a terminal is connected, change its baud rate to match. Later resets and power cycles restore the saved value, with or without an SD card.
5. **UART test** is the other functional item in the same UART submenu. It uses the active console rate.

![Diagnostics UART submenu, UART test and persistent P4 baud selection](images/v1.4/sd-06-uart.png)

The setting uses a **256-byte append-only journal at 0x08007F00–0x08007FFF**, inside BOOT. Each changed saved selection consumes one byte; choosing the already saved value consumes none. At most **256 changes** fit in a fresh journal, and an interrupted invalid record also consumes its slot. When full, the UI reports **`P4 not saved` / `Settings full`** (`ERROR LIST_FULL` on UART), preserving the current and saved settings. The running bootloader does not erase sectors to recycle the journal. A normal application update preserves it; reinstalling BOOT resets it.

Hold **UP + DOWN during power-on/reset** to force **250000** for that boot without overwriting the saved choice. This is useful when the remembered rate is unknown. The setting controls the bootloader's P4 console only. The r9898 installer always initializes its own console at **250000, 8N1**, and the stock application has its own UART initialization.

## 10. If the result differs from the instructions

| Observation | Action |
|---|---|
| Factory route does not reach r9898 | Record the actual factory message and check the prerequisites and card contents. Do not rename RESTORE as a factory update file. |
| Backup is rejected or reports changed contents | Keep the existing files. Check whether the card contains old copies from a different BOOT. Archive real backups before preparing fresh templates; do not bypass verification. |
| `OPERATION REJECTED` / `HARDWARE` | Stop. This is a combined compatibility/protection/supply category, not proof of a specific RDP value. Do not unprotect or mass-erase. |
| r9898 appears again after BOOT was installed | Its application is still present. Use Restart, interrupt the new countdown, and perform the explicit RESTORE steps. |
| File browser order differs | Select by the exact filename, then confirm the selected page title. Do not rely on a fixed list position. |
| Result screen does not react to OK | Release buttons and wait for the automatic return: 3 seconds in v1.4, 1.8 seconds for installer menu results. |
| Console disappears after changing baud | Set the terminal to the newly selected rate. UP+DOWN at startup temporarily forces 250000 if needed. |
| BOOT programming fails or power is lost during it | Keep the backups and logs. BOOT may require SWD recovery; two SD files do not provide an automatic rollback. Apply only the verified sector-specific ST-Link procedure when Flash access is available. |
| ST-Link full readback differs outside BOOT | Do not start the application. Preserve BEFORE, AFTER and the log for diagnosis; do not expand the erase range. |

The published packages contain binaries, documentation, checksums and UI illustrations. Keep printer-specific full dumps, NVM, identity/OTP data, Option byte captures and actual BOOT backups in your own archive; they are not part of the public release.

Independent project; not affiliated with or endorsed by Zortrax.
