# ⌫ Uninstall'd

> **Deep program removal for Windows** — goes where the built-in uninstaller won't.

![Build](https://github.com/hawaiizfynest/uninstalld/actions/workflows/build.yml/badge.svg)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-yellow)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.0.2-red)

Uninstall'd scans your **registry**, **program files**, and **%TEMP%** folder to find and remove every last trace of a program — not just what the stock uninstaller cleans up. It also lets you **move installations between drives** and **back up and restore your registry** before making any changes.

---

## What's New in v1.0.2

### 🐛 Extraction Fix
The project zip previously contained a folder literally named `{src,assets,installer}` — a side effect of Linux brace expansion during packaging. Windows forbids `{`, `,`, and `}` in path names, causing extraction to fail with a *"path component can't contain control characters"* error. This is fixed in v1.0.2. The zip is now built using explicit file paths so this cannot happen again.

---

## Changes in v1.0.1

### 🛡️ Registry Backup Prompt
Before **any** destructive action — deletion or drive move — a mandatory prompt now appears asking how you want to proceed:
- **"🛡 Backup and Continue"** — saves a `.reg` backup of your registry to `%APPDATA%\Uninstalld\backups\` before doing anything
- **"⚠ Continue Without Backup"** — skips the backup and proceeds immediately
- **"Cancel"** — aborts the entire operation; nothing is touched

### 🔄 Registry Restore
A new **"🔄 Restore Registry"** button lives in the top-right of the app. It opens a restore panel where you can browse all saved backups (sorted newest-first with timestamps and file sizes), select one, and re-import it with a single click.

### 📦 Force-Move Between Drives
After scanning, a **"📦 Move to Drive..."** button appears when an install location is detected. It:
- Lists all connected drives with free and total space
- Auto-fills the destination path when you select a drive
- Shows a live space check (turns red if the destination is too small)
- Copies all files to the new location
- **Rewrites registry path entries** — any registry value pointing to the old install path is automatically updated to the new location
- Removes the original folder once the move is complete

---

## Features

### 🔍 Deep Scanner
- Searches `HKLM`, `HKCU`, `HKCR`, and `HKU` for all keys and values tied to the program, including Uninstall entries, App Paths, and software keys
- Checks `Program Files`, `Program Files (x86)`, `%APPDATA%`, `%LOCALAPPDATA%`, and `%ProgramData%` for leftover folders
- Scans `%TEMP%` for leftover installer and runtime files
- Results appear live across three panels as the scan runs

### ☑️ Selective Deletion
- Every result is individually checkable/uncheckable
- Separate toggles for registry entries, files/folders, and temp files
- "Select All" to re-check everything at once

### 📋 Live Operation Log
- Real-time log of every scan hit, deletion, and registry update
- Color-coded: green for success, red for errors

### 🛡️ UAC Elevation
- Automatically requests administrator rights on launch — required for registry access and system folder operations

---

## Installation

Download the latest installer from [Releases](https://github.com/hawaiizfynest/uninstalld/releases):

```
Uninstalld_Setup_v1.0.2.exe
```

- Installs to `C:\Program Files\Uninstall'd\`
- Registers with Windows **Add/Remove Programs**
- Creates **Start Menu** and **Desktop** shortcuts

**Requirements:** Windows 10 or 11 (64-bit)

---

## How to Use

1. Launch **Uninstall'd** (UAC prompt will appear — click Yes)
2. Type the program name in the search bar (e.g. `Discord`, `Spotify`)
3. Click **▶ SCAN** — results appear live across the three panels
4. Review what was found across Registry Entries, Files & Folders, and Temp Files
5. Uncheck anything you want to keep
6. To **remove**: click **🗑 DELETE SELECTED** → choose backup option → confirm
7. To **move to another drive**: click **📦 Move to Drive...** → choose backup option → pick destination → click Move

---

## Registry Backup & Restore

Backups are saved to:
```
%APPDATA%\Uninstalld\backups\
```

Each backup is a pair of `.reg` files:
- `backup_<program>_<timestamp>.reg` — `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion`
- `backup_<program>_<timestamp>.hkcu.reg` — `HKCU\SOFTWARE`

To restore, click **🔄 Restore Registry** in the header, pick a backup from the list, and click **Restore Selected**. Both files re-import automatically. Restart your PC afterwards for full effect.

---

## Building from Source

### Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.10+ | [python.org](https://python.org) |
| PyInstaller | 5.13+ | `pip install pyinstaller` |
| NSIS | 3.x | [nsis.sourceforge.io](https://nsis.sourceforge.io) |

> **PATH note:** After installing Python, pip may warn that a Scripts directory like
> `C:\Users\<you>\AppData\Roaming\Python\Python3xx\Scripts` is not on PATH.
> Fix it by opening **Edit the system environment variables → Environment Variables →
> User variables → Path → New** and pasting that path in. Restart your terminal afterwards.

### One-click build with `build.bat`

`build.bat` handles the entire process in four steps:

```
1. Checks that Python is installed and on PATH
2. Runs:  pip install PyQt6 pyinstaller
3. Runs:  pyinstaller uninstalld.spec --noconfirm
          → outputs dist\uninstalld\uninstalld.exe
4. Detects NSIS and runs:  makensis installer\setup.nsi
          → outputs Uninstalld_Setup_v1.0.2.exe
```

To use it:

```bat
git clone https://github.com/hawaiizfynest/uninstalld.git
cd uninstalld
build.bat
```

If NSIS is not installed, `build.bat` skips step 4, prints a warning, and exits with the
portable `.exe` ready at `dist\uninstalld\uninstalld.exe`. You can run the NSIS step
manually at any time:

```bat
"C:\Program Files (x86)\NSIS\makensis.exe" installer\setup.nsi
```

### Executable only (no `build.bat`)

If you just want the `.exe` without the full script:

```bat
pip install -r requirements.txt
pyinstaller uninstalld.spec --noconfirm
```

Output at `dist\uninstalld\uninstalld.exe`.

---

## Project Structure

```
uninstalld/
├── .github/
│   └── workflows/
│       └── build.yml          ← CI/CD: builds on push, publishes installer on version tag
├── src/
│   ├── main.py                ← Full PyQt6 application
│   └── icon_data.py           ← App icon embedded as base64
├── assets/
│   ├── icon.ico               ← Multi-resolution Windows icon (16px–256px)
│   └── header.bmp             ← NSIS installer banner
├── installer/
│   └── setup.nsi              ← NSIS installer script
├── uninstalld.spec            ← PyInstaller build spec
├── version_info.txt           ← Windows EXE version metadata
├── requirements.txt
├── build.bat                  ← One-click build script
└── github_setup.bat           ← First-time GitHub repo setup
```

---

## Releasing a New Version

Push a version tag — GitHub Actions builds and publishes the installer automatically:

```bash
git tag v1.0.2
git push origin v1.0.2
```

---

## ⚠️ Safety Warning

Uninstall'd **permanently deletes** registry keys and files. The backup prompt exists for a reason — use it. If you're unsure about an entry, uncheck it or cancel and investigate first.

---

## Changelog

### v1.0.2
- Fixed illegal folder name `{src,assets,installer}` being included in the project zip
- Windows was unable to extract the archive due to `{`, `,`, `}` being forbidden path characters
- Rebuilt zip using explicit file paths to prevent this from recurring

### v1.0.1
- Added mandatory registry backup prompt before all destructive actions
- Added registry restore panel (🔄 Restore Registry button in header)
- Added force-move installation between drives with automatic registry path rewriting
- Live disk space check in the Move dialog
- Operation log now covers move and restore actions

### v1.0.0
- Initial release
- Registry scanner (HKLM, HKCU, HKCR, HKU)
- File and folder scanner (Program Files, AppData, ProgramData)
- %TEMP% scanner
- Selective deletion with per-item checkboxes
- Embedded app icon (multi-resolution ICO)
- NSIS installer with Add/Remove Programs registration

---

## License

MIT — see [LICENSE.txt](LICENSE.txt)
