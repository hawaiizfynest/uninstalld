@echo off
REM ============================================================
REM  Uninstall'd — Windows Build Script
REM  Prerequisites: Python 3.10+, PyInstaller, NSIS
REM ============================================================

echo.
echo  ============================================
echo   Uninstall'd Build Script
echo  ============================================
echo.

REM ── Check Python ────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.10+ and add to PATH.
    pause & exit /b 1
)

REM ── Install dependencies ────────────────────────────────────
echo [1/4] Installing Python dependencies...
pip install PyQt6 pyinstaller --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause & exit /b 1
)
echo       Done.

REM ── Clean previous build ────────────────────────────────────
echo [2/4] Cleaning previous build...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
echo       Done.

REM ── Build executable with PyInstaller ───────────────────────
echo [3/4] Building executable (this may take a minute)...
pyinstaller uninstalld.spec --noconfirm
if errorlevel 1 (
    echo [ERROR] PyInstaller build failed.
    pause & exit /b 1
)
echo       Executable built: dist\uninstalld\uninstalld.exe

REM ── Build installer with NSIS ───────────────────────────────
echo [4/4] Building NSIS installer...

REM Check for NSIS in common install locations
set NSIS_PATH=
if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
    set NSIS_PATH="C:\Program Files (x86)\NSIS\makensis.exe"
) else if exist "C:\Program Files\NSIS\makensis.exe" (
    set NSIS_PATH="C:\Program Files\NSIS\makensis.exe"
) else (
    where makensis >nul 2>&1
    if not errorlevel 1 set NSIS_PATH=makensis
)

if "%NSIS_PATH%"=="" (
    echo [WARNING] NSIS not found. Skipping installer creation.
    echo           Install NSIS from https://nsis.sourceforge.io/
    echo           Then run: makensis installer\setup.nsi
    echo.
    echo [OK] Portable executable is ready at dist\uninstalld\uninstalld.exe
    pause & exit /b 0
)

%NSIS_PATH% installer\setup.nsi
if errorlevel 1 (
    echo [ERROR] NSIS build failed.
    pause & exit /b 1
)

echo.
echo  ============================================
echo   Build complete!
echo  ============================================
echo   Installer: Uninstalld_Setup_v1.0.0.exe
echo   Portable:  dist\uninstalld\uninstalld.exe
echo  ============================================
echo.
pause
