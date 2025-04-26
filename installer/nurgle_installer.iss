
!define APPNAME "DeathGuard Assistant"
!define DESCRIPTION "Nurgle-Blessed Lore Cogitator"
!define VERSION "1.0"
!define COMPANY "The Grandfather's Chosen"
!define INSTALLER_NAME "DeathGuard_Assistant_Installer.exe"

SetCompressor /SOLID lzma
Name "${APPNAME}"
OutFile "${INSTALLER_NAME}"
InstallDir "$PROGRAMFILES64\${APPNAME}"
InstallDirRegKey HKLM "Software\${COMPANY}\${APPNAME}" "Install_Dir"
RequestExecutionLevel admin

Page directory
Page instfiles

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "dist\boot_splash.exe"
  File "death_guard.ico"
  File "vox_startup.wav"
  File "glitch_splash.gif"
  File "warpcog_background.bmp"
  File "warhammer_lore.txt"
  File "lore_gui_ollama.py"
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  CreateShortCut "$DESKTOP\DeathGuard Assistant.lnk" "$INSTDIR\boot_splash.exe" "" "$INSTDIR\death_guard.ico"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\boot_splash.exe"
  Delete "$INSTDIR\death_guard.ico"
  Delete "$INSTDIR\vox_startup.wav"
  Delete "$INSTDIR\glitch_splash.gif"
  Delete "$INSTDIR\warpcog_background.bmp"
  Delete "$INSTDIR\warhammer_lore.txt"
  Delete "$INSTDIR\lore_gui_ollama.py"
  Delete "$INSTDIR\Uninstall.exe"
  Delete "$DESKTOP\DeathGuard Assistant.lnk"
  RMDir "$INSTDIR"
SectionEnd
