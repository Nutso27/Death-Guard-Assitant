
@echo off
echo ================================
echo ☣ Rebuilding Final Nurgle Assistant
echo ================================

cd /d "%~dp0"

REM Clean old build artifacts
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

REM Build the GUI assistant
echo [1/2] Building DeathGuard_Lore_v1.1.exe...
pyinstaller lore_gui_ollama.py --onefile --windowed --icon=death_guard.ico --name DeathGuard_Lore_v1.1 ^
--add-data "glitch_splash.gif;." --add-data "warhammer_lore.txt;." --add-data "vox_startup.wav;." --add-data "warpcog_background.bmp;."

REM Build the launcher
echo [2/2] Building DeathGuardLauncher.exe...
pyinstaller DeathGuardLauncher.py --onefile --windowed --icon=death_guard.ico --name DeathGuardLauncher

REM Move compiled .exe files to this directory
move /Y dist\DeathGuard_Lore_v1.1.exe .
move /Y dist\DeathGuardLauncher.exe .

echo.
echo ✅ Build complete. You're ready to compile the installer.
pause
