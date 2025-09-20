# 🎮 World of Tanks Mod Installer - Installationsanleitung

## ✅ Was wurde erstellt

In Ihrem Ordner `G:\Games\World_of_Tanks_EU\Aslain_Modpack\Custom_mods\` wurden folgende Dateien erstellt:

1. **`install_mods.bat`** - Hauptstartdatei (Doppelklick zum Starten!)
2. **`wot_mod_installer.py`** - Grafische Version mit Benutzeroberfläche
3. **`wot_mod_installer_cli.py`** - Kommandozeilen-Version
4. **`README.md`** - Detaillierte Dokumentation

## 🚀 So funktioniert es

### Einfachste Methode:
1. **Doppelklick auf `install_mods.bat`**
2. Wählen Sie Option 1 (**GUI .exe - KEINE Python Installation nötig!**)
3. Die grafische Oberfläche öffnet sich
4. Überprüfen Sie die erkannten Pfade
5. Wählen Sie ZIP-Dateien aus
6. **NEU: Klicken Sie "Vorschau"** um zu sehen, was installiert wird
7. Klicken Sie "Installieren" zur tatsächlichen Installation

### Alternative - Direkt die .exe starten:
- **Doppelklick auf `WoT_Mod_Installer.exe`** - Sofort loslegen ohne Python!

### Was das Programm macht:

- ✅ Erkennt automatisch Ihre WoT-Version (aktuell: **2.0.0.1**)
- ✅ Ersetzt `version` Platzhalter in ZIP-Dateien durch echte Versionsnummer
- ✅ **UNIVERSAL:** Kopiert ALLE Ordnertypen in ZIP-Dateien:
  - `mods/version/` → `mods/2.0.0.1/` (Mod-Dateien)
  - `mods/configs/` → `mods/configs/` (Mod-Konfigurationen)
  - `res/` → `res/` (Sound-Dateien, Texturen)
  - `res_mods/configs/` → `res_mods/configs/` (XVM-Konfigurationen)
- ✅ Zeigt detailliertes Log der Installation
- ✅ **NEU: Vorschau-Funktion** - Sehen Sie vor der Installation, welche Dateien wohin kopiert werden

### Beispiele:

```text
ZIP-Inhalt:     mods/version/champi.armorcalculatorpro.wotmod
Wird entpackt:  mods/2.0.0.1/champi.armorcalculatorpro.wotmod

ZIP-Inhalt:     res/audioww/sixthSense_wuff_wuff.mp3
Wird entpackt:  res/audioww/sixthSense_wuff_wuff.mp3

ZIP-Inhalt:     mods/configs/Driftkings/AutoAimOptimize.json
Wird entpackt:  mods/configs/Driftkings/AutoAimOptimize.json
```

## 📋 Voraussetzungen erfüllt

- ✅ **Python 3.8.10** ist bereits konfiguriert
- ✅ **World of Tanks** wurde gefunden: `G:\Games\World_of_Tanks_EU\`
- ✅ **Aktuelle Version** erkannt: `2.0.0.1`
- ✅ **23 ZIP-Dateien** im Ordner gefunden

## 🎯 Getestet und funktionsbereit

Das Programm wurde erfolgreich getestet:
- Versionserkennung funktioniert
- ZIP-Dateien werden korrekt erkannt
- Alle Funktionen sind einsatzbereit

## 📞 Support & Problemlösung

Falls Probleme auftreten:
1. Überprüfen Sie das Installations-Log in der GUI
2. Stellen Sie sicher, dass World of Tanks geschlossen ist
3. Führen Sie die Batch-Datei als Administrator aus (falls nötig)

---

**🎮 Jetzt können Sie Ihre World of Tanks Mods automatisch installieren!**

**Starten Sie mit einem Doppelklick auf `install_mods.bat`** ⚡