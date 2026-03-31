; ============================================================
;  Uninstall'd — NSIS Installer Script
;  Installs the app to Program Files and adds Start Menu + Uninstall entry
; ============================================================

!define APP_NAME      "Uninstall'd"
!define APP_EXE       "uninstalld.exe"
!define APP_VERSION   "1.0.2"
!define APP_PUBLISHER "Uninstall'd"
!define APP_URL       "https://github.com/hawaiizfynest/uninstalld"

; Compression
SetCompressor /SOLID lzma
SetCompressorDictSize 32

; Modern UI
!include "MUI2.nsh"
!include "x64.nsh"

; General settings
Name        "${APP_NAME}"
OutFile     "Uninstalld_Setup_v${APP_VERSION}.exe"
InstallDir  "$PROGRAMFILES64\${APP_NAME}"
InstallDirRegKey HKLM "Software\${APP_NAME}" "InstallPath"
RequestExecutionLevel admin
BrandingText "${APP_NAME} v${APP_VERSION}"
Unicode True

; ── MUI Pages ──────────────────────────────────────────────
!define MUI_ABORTWARNING
!define MUI_ICON   "..\assets\icon.ico"
!define MUI_UNICON "..\assets\icon.ico"

!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "..\assets\header.bmp"
!define MUI_HEADERIMAGE_RIGHT

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

; ── Install Section ─────────────────────────────────────────
Section "Main Application" SecMain
  SectionIn RO   ; Required — cannot be unchecked

  SetOutPath "$INSTDIR"

  ; Copy all files from the dist folder (PyInstaller output)
  File /r "..\dist\uninstalld\*.*"

  ; Write registry uninstall info
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
              "DisplayName"          "${APP_NAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
              "DisplayVersion"       "${APP_VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
              "Publisher"            "${APP_PUBLISHER}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
              "URLInfoAbout"         "${APP_URL}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
              "InstallLocation"      "$INSTDIR"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
              "UninstallString"      '"$INSTDIR\Uninstall.exe"'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
              "DisplayIcon"          '"$INSTDIR\${APP_EXE}"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
               "NoModify"           1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
               "NoRepair"           1

  ; Store install path
  WriteRegStr HKLM "Software\${APP_NAME}" "InstallPath" "$INSTDIR"

  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ; Start Menu shortcut
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortcut  "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" \
                  "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0
  CreateShortcut  "$SMPROGRAMS\${APP_NAME}\Uninstall ${APP_NAME}.lnk" \
                  "$INSTDIR\Uninstall.exe"

  ; Desktop shortcut (optional — user can skip)
  CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0

SectionEnd

; ── Uninstall Section ───────────────────────────────────────
Section "Uninstall"

  ; Remove installed files
  RMDir /r "$INSTDIR"

  ; Remove Start Menu
  RMDir /r "$SMPROGRAMS\${APP_NAME}"

  ; Remove Desktop shortcut
  Delete "$DESKTOP\${APP_NAME}.lnk"

  ; Remove registry entries
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
  DeleteRegKey HKLM "Software\${APP_NAME}"

  ; Remove App Paths entry
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\App Paths\${APP_EXE}"

SectionEnd
