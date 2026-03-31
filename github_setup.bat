@echo off
REM ============================================================
REM  Uninstall'd — GitHub Setup Script
REM  Creates the repo on GitHub and pushes all code
REM  Run this from inside the uninstalld\ project folder
REM ============================================================

echo.
echo  ============================================
echo   Uninstall'd — GitHub Setup
echo  ============================================
echo.

REM ── Check git ───────────────────────────────────────────────
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git not found.
    echo         Install from https://git-scm.com/download/win
    pause & exit /b 1
)

REM ── Check GitHub CLI ────────────────────────────────────────
gh --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] GitHub CLI ^(gh^) not found.
    echo         Install from https://cli.github.com
    echo         Then run: gh auth login
    pause & exit /b 1
)

REM ── Check login ─────────────────────────────────────────────
gh auth status >nul 2>&1
if errorlevel 1 (
    echo [INFO] Not logged into GitHub CLI. Launching login...
    gh auth login
)

echo [1/4] Initialising local git repo...
git init
git add .
git commit -m "Initial commit - Uninstall'd v1.0.0"

echo [2/4] Creating public GitHub repository...
gh repo create uninstalld --public --description "Deep program removal tool for Windows — scans registry, files, and %%TEMP%% for all traces" --source=. --remote=origin

echo [3/4] Pushing code...
git push -u origin main

echo [4/4] Opening repo in browser...
gh repo view --web

echo.
echo  ============================================
echo   Done! Repo live at:
echo   https://github.com/hawaiizfynest/uninstalld
echo  ============================================
echo.
pause
