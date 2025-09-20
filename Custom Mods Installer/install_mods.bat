@echo off
title World of Tanks Mod Installer
chcp 65001 >nul
echo.
echo ==========================================
echo    World of Tanks Mod Installer
echo ==========================================
echo.

:: Prüfe ob Python verfügbar ist
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python ist nicht installiert oder nicht im PATH verfügbar.
    echo Bitte installieren Sie Python 3.x von https://python.org
    pause
    exit /b 1
)

:: Wechsle ins Verzeichnis der Batch-Datei
cd /d "%~dp0"

echo Verfügbare Optionen:
echo.
echo 1. GUI-Version v2.1 (.exe - SMART Auto-Setup!)
echo 2. GUI-Version starten (Python-Skript)
echo 3. Kommandozeilen-Version (alle ZIP-Dateien)
echo 4. ZIP-Dateien nur auflisten
echo 5. Vorschau anzeigen (ohne Installation)
echo 6. Einzelne ZIP-Dateien auswählen
echo.

set /p choice="Bitte wählen Sie eine Option (1-6): "

if "%choice%"=="1" (
    echo.
    echo Starte GUI-Version v2.1 (.exe) mit Smart Auto-Setup...
    WoT_Mod_Installer_v2.1.exe
) else if "%choice%"=="2" (
    echo.
    echo Starte GUI-Version (Python-Skript)...
    python wot_mod_installer.py
) else if "%choice%"=="3" (
    echo.
    echo Starte Installation aller ZIP-Dateien...
    python wot_mod_installer_cli.py
) else if "%choice%"=="4" (
    echo.
    echo Verfügbare ZIP-Dateien:
    python wot_mod_installer_cli.py --list-only
) else if "%choice%"=="5" (
    echo.
    echo Vorschau aller ZIP-Dateien:
    python wot_mod_installer_cli.py --preview
) else if "%choice%"=="6" (
    echo.
    echo Verfügbare ZIP-Dateien:
    python wot_mod_installer_cli.py --list-only
    echo.
    set /p zipfiles="Geben Sie die Dateinamen ein (getrennt durch Leerzeichen): "
    if not "%zipfiles%"=="" (
        python wot_mod_installer_cli.py --zip-files %zipfiles%
    )
) else (
    echo Ungültige Auswahl.
)

echo.
pause