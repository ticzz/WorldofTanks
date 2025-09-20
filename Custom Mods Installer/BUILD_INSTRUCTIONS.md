# 🏗️ Build Instructions - WoT Mod Installer

Diese Anleitung erklärt, wie Sie eigenständige .exe-Dateien des World of Tanks Mod Installers erstellen können.

## 📋 Voraussetzungen

1. **Python 3.8 oder höher** muss installiert sein
   - Download: https://python.org
   - ⚠️ **Wichtig**: Bei der Installation "Add Python to PATH" aktivieren

2. **PyInstaller installieren:**
   ```batch
   pip install pyinstaller
   ```

## 🔧 GUI-Version (.exe) erstellen

### Standard-Version
```batch
pyinstaller --onefile --windowed --name "WoT_Mod_Installer_v2.0" wot_mod_installer.py
```

### Mit Smart Auto-Setup (empfohlen)
```batch
pyinstaller --onefile --windowed --name "WoT_Mod_Installer_v2.1" wot_mod_installer.py
```

## 💻 CLI-Version (.exe) erstellen

```batch
pyinstaller --onefile --name "WoT_Mod_Installer_CLI" wot_mod_installer_cli.py
```

## ⚙️ PyInstaller Optionen erklärt

| Option | Beschreibung |
|--------|-------------|
| `--onefile` | Erstellt eine einzelne .exe-Datei (empfohlen) |
| `--windowed` | Versteckt das Konsolen-Fenster (nur für GUI) |
| `--name` | Name der resultierenden .exe-Datei |

## 📁 Build-Ausgabe

Nach erfolgreichem Build finden Sie:

```
📁 dist/
  └── WoT_Mod_Installer_v2.1.exe  ← Fertige .exe-Datei

📁 build/                          ← Temporäre Build-Dateien
📄 WoT_Mod_Installer_v2.1.spec     ← PyInstaller Konfiguration
```

## 🚀 Verwendung der .exe

Die erstellte .exe-Datei:
- ✅ Läuft **ohne Python-Installation** auf jedem Windows-System
- ✅ Enthält alle benötigten Python-Bibliotheken
- ✅ Kann überall hin kopiert und verteilt werden
- ✅ Startet schneller als das Python-Skript

## 🛠️ Erweiterte Build-Optionen

### Mit benutzerdefiniertem Icon
```batch
pyinstaller --onefile --windowed --icon=icon.ico --name "WoT_Mod_Installer" wot_mod_installer.py
```

### Debug-Version (zeigt Konsole)
```batch
pyinstaller --onefile --name "WoT_Mod_Installer_Debug" wot_mod_installer.py
```

### Mit zusätzlichen Dateien
```batch
pyinstaller --onefile --windowed --add-data "config.json;." --name "WoT_Mod_Installer" wot_mod_installer.py
```

## 🔍 Problembehandlung

### "PyInstaller nicht gefunden"
```batch
# PyInstaller installieren
pip install pyinstaller

# Bei Problemen: Upgrade
pip install --upgrade pyinstaller
```

### ".exe startet nicht"
1. **Debug-Version erstellen** (ohne `--windowed`)
2. **Windows Defender** temporär deaktivieren
3. **Antivirus-Software** überprüfen

### "Fehlende Module"
```batch
# Bei importierten Modulen die nicht erkannt werden
pyinstaller --onefile --windowed --hidden-import tkinter --name "WoT_Mod_Installer" wot_mod_installer.py
```

## 📦 Verteilung

Die .exe-Datei kann:
- 📤 Per E-Mail verschickt werden
- 🌐 Im Internet hochgeladen werden  
- 💾 auf USB-Stick kopiert werden
- 📂 Direkt von andere Benutzern verwendet werden

**Keine zusätzliche Software erforderlich!**

## 🔄 Automatisierung

Sie können einen Build-Script erstellen:

**build_all.bat:**
```batch
@echo off
echo Building WoT Mod Installer...

REM GUI Version
pyinstaller --onefile --windowed --name "WoT_Mod_Installer_v2.1" wot_mod_installer.py

REM CLI Version  
pyinstaller --onefile --name "WoT_Mod_Installer_CLI" wot_mod_installer_cli.py

echo Build complete! Check dist/ folder
pause
```

---

**Happy Building! 🚀**