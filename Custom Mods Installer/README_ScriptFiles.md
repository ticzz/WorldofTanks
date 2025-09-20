# World of Tanks Mod Installer

Ein automatisches Installationsprogramm für World of Tanks Mods, das ZIP-Dateien entpackt und den "version" Platzhalter durch die aktuelle Spielversion ersetzt.

## 🚀 Schnellstart

1. **Doppelklick auf `install_mods.bat`** - Das ist der einfachste Weg!
2. Wählen Sie Option 1 für die grafische Benutzeroberfläche
3. Überprüfen Sie die Pfade und klicken Sie "Installieren"

## 📋 Voraussetzungen

- **Python 3.6+** muss installiert sein
- World of Tanks muss installiert sein
- ZIP-Dateien mit Mods im gleichen Ordner

## 🔧 Verwendung

### Option 1: Grafische Benutzeroberfläche (Empfohlen)
```batch
install_mods.bat
# Dann Option 1 wählen
```

Oder direkt:
```batch
python wot_mod_installer.py
```

**Features der GUI:**
- ✅ Automatische Erkennung der WoT-Installation
- ✅ Übersichtliche Dateiauswahl
- ✅ Installation-Log in Echtzeit
- ✅ Fortschrittsanzeige
- ✅ Konfiguration wird gespeichert

### Option 2: Kommandozeile

**Alle ZIP-Dateien installieren:**
```batch
python wot_mod_installer_cli.py
```

**Nur verfügbare Dateien auflisten:**
```batch
python wot_mod_installer_cli.py --list-only
```

**Spezifische Dateien installieren:**
```batch
python wot_mod_installer_cli.py --zip-files "AchievementNotification_1.2.3.zip" "AutoAimOptimize.zip"
```

**Anderen WoT-Pfad verwenden:**
```batch
python wot_mod_installer_cli.py --wot-path "C:\Games\World_of_Tanks"
```

**ZIP-Dateien aus anderem Ordner:**
```batch
python wot_mod_installer_cli.py --zip-folder "C:\Downloads\Mods"
```

## 📁 Wie es funktioniert

### Version Platzhalter
Das Programm erkennt automatisch Ihre aktuelle World of Tanks Version (z.B. `2.0.0.1`) und ersetzt alle `version` Ordner in den ZIP-Dateien entsprechend.

**Beispiel:**
```
ZIP-Inhalt:     mods/version/mod_datei.wotmod
Wird zu:        mods/2.0.0.1/mod_datei.wotmod
```

### Unterstützte Strukturen
- ✅ `mods/version/datei.wotmod`
- ✅ `mods/version/unterordner/datei.py`
- ✅ `res/audioww/sound.mp3`
- ✅ Beliebige andere Strukturen

## 🛠️ Problembehandlung

### "Python ist nicht installiert"
1. Laden Sie Python von https://python.org herunter
2. Aktivieren Sie "Add Python to PATH" bei der Installation
3. Starten Sie die Eingabeaufforderung neu

### "World of Tanks Version nicht erkannt"
1. Überprüfen Sie den WoT-Installationspfad
2. Stellen Sie sicher, dass ein `mods` Ordner existiert
3. Es sollte ein Unterordner mit Versionsnummer (z.B. `2.0.0.1`) vorhanden sein

### "ZIP-Datei kann nicht entpackt werden"
1. Überprüfen Sie, ob die ZIP-Datei beschädigt ist
2. Stellen Sie sicher, dass Sie Schreibrechte im WoT-Ordner haben
3. Schließen Sie World of Tanks vor der Installation

### "Mod funktioniert nicht im Spiel"
1. Überprüfen Sie, ob die Dateien im richtigen Versionsordner sind
2. Manche Mods benötigen zusätzliche Abhängigkeiten
3. Prüfen Sie das Installations-Log auf Fehler

## 📂 Dateien

| Datei | Beschreibung |
|-------|-------------|
| `wot_mod_installer.py` | Hauptprogramm mit grafischer Oberfläche |
| `wot_mod_installer_cli.py` | Kommandozeilen-Version |
| `install_mods.bat` | Windows-Batch-Datei für einfache Nutzung |
| `installer_config.json` | Konfigurationsdatei (wird automatisch erstellt) |

## ⚙️ Konfiguration

Die GUI-Version speichert Ihre Einstellungen automatisch in `installer_config.json`:

```json
{
  "wot_path": "G:\\Games\\World_of_Tanks_EU",
  "zip_folder": "G:\\Games\\World_of_Tanks_EU\\Aslain_Modpack\\Custom_mods"
}
```

## 🔒 Sicherheit

- Das Programm überschreibt nur Dateien in den entsprechenden Mod-Ordnern
- Es werden keine Systemdateien verändert
- Backup der ursprünglichen Dateien wird empfohlen

## 🏗️ EXE-Datei erstellen (für Entwickler)

Wenn Sie eine eigenständige .exe-Datei ohne Python-Installation erstellen möchten, finden Sie detaillierte Anweisungen in der Datei **BUILD_INSTRUCTIONS.md**.

**Kurz:** 
- Python 3.8+ und PyInstaller erforderlich
- `pyinstaller --onefile --windowed --name "WoT_Mod_Installer_v2.1" wot_mod_installer.py`
- Ergebnis: Standalone .exe ohne Python-Abhängigkeit

## 📝 Changelog

### Version 2.3 (September 2025)
- ✅ **Intelligente Versionserkennung** - Automatische Aktualisierung alter Versionsnummern in ZIP-Dateien
- ✅ **Erweiterte Kompatibilität** - Behandelt sowohl "version" Platzhalter als auch spezifische Versionsnummern

### Version 2.2 (September 2025)
- ✅ **Intelligente Pfad-Erkennung** - Funktioniert mit und ohne Aslain's Modpack
- ✅ **Automatische Ordner-Erstellung** - Custom_mods oder Custom_Mods je nach Installation

### Version 2.1 (September 2025)
- ✅ **Standalone .exe-Versionen** - Kein Python mehr erforderlich!
- ✅ **Smart Auto-Setup** - Automatische WoT-Erkennung und Ordner-Erstellung
- ✅ **Mod-Vorschau** - ZIP-Inhalte vor Installation anzeigen
- ✅ **Universelle Mod-Unterstützung** - Alle Mod-Typen (mods/, res/, configs/)
- ✅ **Erweiterte Launcher** - 6 verschiedene Start-Optionen

### Version 1.0
- ✅ Automatische Version-Erkennung
- ✅ GUI und CLI Versionen
- ✅ Batch-Datei für einfache Nutzung
- ✅ Unterstützung für "version" Platzhalter
- ✅ Detailliertes Logging
- ✅ Konfigurationsspeicherung

## 🤝 Support

Bei Problemen:
1. Überprüfen Sie das Installations-Log
2. Stellen Sie sicher, dass alle Voraussetzungen erfüllt sind
3. Testen Sie mit einer einzelnen ZIP-Datei

---

**Viel Spaß beim Modding! 🎮**
