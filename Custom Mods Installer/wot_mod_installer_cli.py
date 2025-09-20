#!/usr/bin/env python3
"""
World of Tanks Mod Installer - Kommandozeilenversion
Einfaches Script zum automatischen Installieren von WoT Mods
"""

import os
import zipfile
import shutil
from pathlib import Path
import re
import argparse
from datetime import datetime


def log_message(message):
    """Ausgabe mit Zeitstempel"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")


def detect_wot_version(wot_path):
    """Erkenne die aktuelle World of Tanks Version"""
    try:
        mods_path = Path(wot_path) / "mods"
        if not mods_path.exists():
            print(f"Fehler: Mods-Ordner nicht gefunden: {mods_path}")
            return None
        
        # Suche nach Versionsordnern (Format: x.x.x.x)
        version_pattern = re.compile(r'^\d+\.\d+\.\d+\.\d+$')
        versions = []
        
        for item in mods_path.iterdir():
            if item.is_dir() and version_pattern.match(item.name):
                versions.append(item.name)
        
        if versions:
            # Sortiere Versionen und nimm die neueste
            versions.sort(key=lambda x: [int(n) for n in x.split('.')], reverse=True)
            latest_version = versions[0]
            log_message(f"Version erkannt: {latest_version}")
            return latest_version
        else:
            print("Fehler: Keine gültige Spielversion im mods-Ordner gefunden")
            return None
            
    except Exception as e:
        print(f"Fehler beim Erkennen der Version: {e}")
        return None


def preview_mod_installation(zip_file_path, wot_base_path, current_version):
    """Zeige eine Vorschau was installiert werden würde, ohne zu installieren"""
    try:
        print(f"\nVorschau für: {zip_file_path.name}")
        print("=" * 50)
        
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                if member.endswith('/') or member.endswith('\\'):
                    continue  # Überspringe Ordner
                    
                # Alle Dateien werden kopiert, aber "version" wird durch aktuelle Spielversion ersetzt
                if "/version/" in member or "\\version\\" in member:
                    # Ersetze "version" durch aktuelle Spielversion
                    target_path = member.replace("/version/", f"/{current_version}/").replace("\\version\\", f"\\{current_version}\\")
                    print(f"  {member} → {target_path}")
                else:
                    # Normale Datei - wird direkt kopiert (res/, mods/configs/, res_mods/, etc.)
                    print(f"  {member}")
        
        return True
        
    except Exception as e:
        print(f"Fehler bei Vorschau von {zip_file_path.name}: {e}")
        return False


def install_mod(zip_file_path, wot_base_path, current_version):
    """Installiere eine einzelne Mod-ZIP-Datei"""
    try:
        log_message(f"Installiere: {zip_file_path.name}")
        
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                # Überspringe Ordner
                if member.endswith('/') or member.endswith('\\'):
                    continue
                
                # Alle Dateien werden kopiert, aber "version" wird durch aktuelle Spielversion ersetzt
                if "/version/" in member or "\\version\\" in member:
                    # Ersetze "version" durch aktuelle Spielversion
                    target_path = member.replace("/version/", f"/{current_version}/").replace("\\version\\", f"\\{current_version}\\")
                else:
                    # Normale Datei - wird direkt kopiert (res/, mods/configs/, res_mods/, etc.)
                    target_path = member
                
                # Vollständiger Zielpfad (direkt in WoT Hauptordner)
                full_target_path = wot_base_path / target_path
                
                # Erstelle Zielverzeichnis falls notwendig
                full_target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Extrahiere Datei
                with zip_ref.open(member) as source:
                    with open(full_target_path, 'wb') as target:
                        target.write(source.read())
                
                # Log-Ausgabe
                if target_path != member:
                    print(f"  {member} → {target_path}")
                else:
                    print(f"  → {target_path}")
        
        log_message(f"✓ {zip_file_path.name} erfolgreich installiert")
        return True
        
    except Exception as e:
        log_message(f"✗ Fehler bei {zip_file_path.name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="World of Tanks Mod Installer")
    parser.add_argument("--wot-path", default="G:\\Games\\World_of_Tanks_EU", 
                        help="Pfad zur World of Tanks Installation")
    parser.add_argument("--zip-folder", default=".", 
                        help="Ordner mit den ZIP-Dateien")
    parser.add_argument("--zip-files", nargs="*", 
                        help="Spezifische ZIP-Dateien (optional, sonst alle)")
    parser.add_argument("--list-only", action="store_true", 
                        help="Nur verfügbare ZIP-Dateien auflisten")
    parser.add_argument("--preview", action="store_true", 
                        help="Vorschau anzeigen ohne zu installieren")
    
    args = parser.parse_args()
    
    # Validiere World of Tanks Pfad
    wot_path = Path(args.wot_path)
    if not wot_path.exists():
        print(f"Fehler: World of Tanks Pfad existiert nicht: {wot_path}")
        return 1
    
    # Erkenne aktuelle Version
    current_version = detect_wot_version(wot_path)
    if not current_version:
        return 1
    
    # Validiere ZIP-Ordner
    zip_folder = Path(args.zip_folder)
    if not zip_folder.exists():
        print(f"Fehler: ZIP-Ordner existiert nicht: {zip_folder}")
        return 1
    
    # Finde ZIP-Dateien
    if args.zip_files:
        zip_files = [zip_folder / filename for filename in args.zip_files]
        # Validiere dass alle Dateien existieren
        for zip_file in zip_files:
            if not zip_file.exists():
                print(f"Fehler: ZIP-Datei nicht gefunden: {zip_file}")
                return 1
    else:
        zip_files = list(zip_folder.glob("*.zip"))
        zip_files.sort()
    
    if not zip_files:
        print("Keine ZIP-Dateien gefunden.")
        return 1
    
    # Liste ZIP-Dateien auf
    print(f"\nGefundene ZIP-Dateien ({len(zip_files)}):")
    for i, zip_file in enumerate(zip_files, 1):
        print(f"  {i:2d}. {zip_file.name}")
    
    if args.list_only:
        return 0
    
    if args.preview:
        print(f"\n=== VORSCHAU (keine Installation) ===")
        for zip_file in zip_files:
            preview_mod_installation(zip_file, wot_path, current_version)
        return 0
    
    # Bestätigung
    print(f"\nWorld of Tanks Pfad: {wot_path}")
    print(f"Aktuelle Version: {current_version}")
    print(f"Zielordner für mods: {wot_path / 'mods' / current_version}")
    print(f"Zielordner für res_mods: {wot_path / 'res_mods' / current_version}")
    
    response = input(f"\nMöchten Sie {len(zip_files)} Mod(s) installieren? (j/N): ")
    if response.lower() not in ['j', 'ja', 'y', 'yes']:
        print("Installation abgebrochen.")
        return 0
    
    # Installation
    wot_base_path = wot_path  # Direkt in den WoT Hauptordner
    success_count = 0
    error_count = 0
    
    print(f"\n=== Installation gestartet ===")
    
    for zip_file in zip_files:
        if install_mod(zip_file, wot_base_path, current_version):
            success_count += 1
        else:
            error_count += 1
    
    print(f"\n=== Installation abgeschlossen ===")
    print(f"Erfolgreich: {success_count}")
    print(f"Fehler: {error_count}")
    
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    exit(main())