# ⌫ Uninstall'd

> **Deep program removal for Windows** — goes where the built-in uninstaller won't.

![Build](https://github.com/hawaiizfynest/uninstalld/actions/workflows/build.yml/badge.svg)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

Uninstall'd scans your **registry**, **program files**, and **%TEMP%** folder to find and remove every last trace of a program — not just what the stock uninstaller cleans up.

---

## Features

- 🔍 **Registry Scanner** — searches `HKLM`, `HKCU`, `HKCR`, and `HKU` for keys and values tied to the program, including Uninstall entries and App Paths
- 📁 **File & Folder Scanner** — checks `Program Files`, `Program Files (x86)`, `%APPDATA%`, `%LOCALAPPDATA%`, and `%ProgramData%`
- 🗂️ **Temp File Scanner** — finds leftover installer and runtime files in `%TEMP%`
- ☑️ **Selective Deletion** — check or uncheck individual items before committing
- 📋 **Live Deletion Log** — see exactly what was removed and what failed, in real time
- 🛡️ **UAC Elevation** — automatically requests admin rights on launch

---

## Installation

Download the latest installer from [Releases](https://github.com/hawaiizfynest/uninstalld/releases):

```
Uninstalld_Setup_v1.0.0.exe
```

Installs to `C:\Program Files\Uninstall'd\` and registers with Windows Add/Remove Programs.

**Requirements:** Windows 10 or 11 (64-bit)

---

## Building from Source

```bat
git clone https://github.com/hawaiizfynest/uninstalld.git
cd uninstalld
build.bat
```

Requires Python 3.10+, PyInstaller, and [NSIS](https://nsis.sourceforge.io).

---

## Releasing a New Version

Push a version tag — GitHub Actions builds and publishes the installer automatically:

```bash
git tag v1.0.1
git push origin v1.0.1
```

---

## ⚠️ Warning

Uninstall'd **permanently deletes** registry keys and files. Always review results before clicking Delete. There is no undo.

---

## License

MIT — see [LICENSE.txt](LICENSE.txt)
