#!/usr/bin/env python3
"""
World of Tanks Mod Installer
Automatisches Entpacken von Mod-ZIP-Dateien in den korrekten WoT Ordner.
Ersetzt den "version" Platzhalter durch die aktuelle Spielversion.
"""

import os
import zipfile
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
from pathlib import Path
import re
import json
from datetime import datetime


class WoTModInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("World of Tanks Mod Installer v2.1")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Konfiguration
        self.config_file = "installer_config.json"
        self.load_config()
        
        # Variablen - mit intelligenter Pfad-Erkennung
        default_wot_path = self.config.get("wot_path", "G:\\Games\\World_of_Tanks_EU")
        self.wot_path = tk.StringVar(value=default_wot_path)
        self.current_version = tk.StringVar()
        
        # Smart ZIP-Ordner Bestimmung
        default_zip_folder = self.get_smart_zip_folder(default_wot_path)
        self.zip_folder = tk.StringVar(value=default_zip_folder)
        
        self.setup_ui()
        self.detect_wot_version()
        
    def get_smart_zip_folder(self, wot_path):
        """Bestimme intelligenten Standard-Pfad für ZIP-Ordner"""
        try:
            if wot_path and os.path.exists(wot_path):
                # Prüfe ob bereits ein Aslain_Modpack Ordner existiert
                aslain_path = os.path.join(wot_path, "Aslain_Modpack")
                if os.path.exists(aslain_path):
                    # Aslain's Modpack ist installiert - verwende Custom_mods Unterordner
                    custom_mods_path = os.path.join(aslain_path, "Custom_mods")
                    if not os.path.exists(custom_mods_path):
                        os.makedirs(custom_mods_path, exist_ok=True)
                        print(f"Custom Mods Ordner erstellt: {custom_mods_path}")
                    return custom_mods_path
                else:
                    # Normale WoT Installation - verwende einfachen Mods-Ordner
                    mods_path = os.path.join(wot_path, "Custom_Mods")
                    if not os.path.exists(mods_path):
                        os.makedirs(mods_path, exist_ok=True)
                        print(f"Custom Mods Ordner erstellt: {mods_path}")
                    return mods_path
            else:
                # Fallback auf aktuelles Verzeichnis
                return self.config.get("zip_folder", os.getcwd())
        except Exception as e:
            print(f"Fehler bei Smart Pfad-Erkennung: {e}")
            return self.config.get("zip_folder", os.getcwd())
    
    def smart_version_replacement(self, file_path, current_version):
        """Intelligente Versionserkennung und -ersetzung in Dateipfaden"""
        import re
        
        # 1. Ersetze expliziten "version" Platzhalter
        if "/version/" in file_path or "\\version\\" in file_path:
            return file_path.replace("/version/", f"/{current_version}/").replace("\\version\\", f"\\{current_version}\\")
        
        # 2. Erkenne und ersetze existierende Versionsnummern im mods/ Ordner
        # Vereinfachtes Pattern für bessere Kompatibilität
        if "mods/" in file_path:
            # Forward slash Pattern
            pattern = r'mods/\d+\.\d+\.\d+\.\d+/'
            if re.search(pattern, file_path):
                return re.sub(pattern, f'mods/{current_version}/', file_path)
        
        if "mods\\" in file_path:
            # Backslash Pattern (Windows)
            pattern = r'mods\\\d+\.\d+\.\d+\.\d+\\'
            if re.search(pattern, file_path):
                return re.sub(pattern, f'mods\\{current_version}\\', file_path)
        
        # 3. Keine Änderung nötig
        return file_path
        
    def load_config(self):
        """Lade Konfiguration aus JSON-Datei"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = {}
        except Exception as e:
            self.config = {}
            print(f"Fehler beim Laden der Konfiguration: {e}")
    
    def save_config(self):
        """Speichere Konfiguration in JSON-Datei"""
        try:
            self.config["wot_path"] = self.wot_path.get()
            self.config["zip_folder"] = self.zip_folder.get()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern der Konfiguration: {e}")
    
    def setup_ui(self):
        """Erstelle die Benutzeroberfläche"""
        # Hauptframe
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Konfiguriere Grid-Gewichte
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # WoT Pfad
        ttk.Label(main_frame, text="World of Tanks Pfad:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.wot_path, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=5)
        ttk.Button(main_frame, text="Durchsuchen", command=self.browse_wot_path).grid(row=0, column=2, padx=(5, 0), pady=5)
        
        # Aktuelle Version
        ttk.Label(main_frame, text="Aktuelle Version:").grid(row=1, column=0, sticky=tk.W, pady=5)
        version_frame = ttk.Frame(main_frame)
        version_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        version_frame.columnconfigure(0, weight=1)
        
        ttk.Label(version_frame, textvariable=self.current_version, font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(version_frame, text="Neu erkennen", command=self.detect_wot_version).grid(row=0, column=1, padx=(10, 0))
        
        # ZIP-Ordner
        ttk.Label(main_frame, text="ZIP-Dateien Ordner:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.zip_folder, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=5)
        ttk.Button(main_frame, text="Durchsuchen", command=self.browse_zip_folder).grid(row=2, column=2, padx=(5, 0), pady=5)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        # Dateien-Liste
        ttk.Label(main_frame, text="Verfügbare ZIP-Dateien:").grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        # Listbox mit Scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, height=8)
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Liste aktualisieren", command=self.refresh_file_list).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Alle auswählen", command=self.select_all_files).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Auswahl aufheben", command=self.deselect_all_files).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Vorschau", command=self.preview_selected_mods).pack(side=tk.LEFT, padx=(20, 0))
        ttk.Button(button_frame, text="Installieren", command=self.install_selected_mods, style="Accent.TButton").pack(side=tk.LEFT, padx=(10, 0))
        
        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Log-Bereich
        ttk.Label(main_frame, text="Installation Log:").grid(row=8, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=8, wrap=tk.WORD)
        self.log_text.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(9, weight=1)
        
        # Initial laden
        self.refresh_file_list()
    
    def log_message(self, message):
        """Füge Nachricht zum Log hinzu"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def browse_wot_path(self):
        """Durchsuche nach World of Tanks Installationsordner"""
        folder = filedialog.askdirectory(
            title="World of Tanks Installationsordner auswählen",
            initialdir=self.wot_path.get()
        )
        if folder:
            self.wot_path.set(folder)
            
            # Aktualisiere automatisch den ZIP-Ordner basierend auf neuem WoT-Pfad
            smart_zip_folder = self.get_smart_zip_folder(folder)
            self.zip_folder.set(smart_zip_folder)
            
            self.detect_wot_version()
            self.refresh_file_list()
            self.save_config()
            
            self.log_message(f"WoT-Pfad aktualisiert: {folder}")
            self.log_message(f"ZIP-Ordner automatisch gesetzt: {smart_zip_folder}")
    
    def browse_zip_folder(self):
        """Durchsuche nach ZIP-Dateien Ordner"""
        folder = filedialog.askdirectory(
            title="Ordner mit ZIP-Dateien auswählen",
            initialdir=self.zip_folder.get()
        )
        if folder:
            self.zip_folder.set(folder)
            self.refresh_file_list()
            self.save_config()
    
    def detect_wot_version(self):
        """Erkenne die aktuelle World of Tanks Version"""
        try:
            mods_path = Path(self.wot_path.get()) / "mods"
            if not mods_path.exists():
                self.current_version.set("Nicht gefunden - Mods-Ordner existiert nicht")
                return
            
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
                self.current_version.set(latest_version)
                self.log_message(f"Version erkannt: {latest_version}")
            else:
                self.current_version.set("Keine Version gefunden")
                self.log_message("Keine gültige Spielversion im mods-Ordner gefunden")
                
        except Exception as e:
            self.current_version.set(f"Fehler: {str(e)}")
            self.log_message(f"Fehler beim Erkennen der Version: {e}")
    
    def refresh_file_list(self):
        """Aktualisiere die Liste der ZIP-Dateien"""
        self.file_listbox.delete(0, tk.END)
        
        try:
            zip_path = Path(self.zip_folder.get())
            if not zip_path.exists():
                self.log_message(f"ZIP-Ordner existiert nicht: {zip_path}")
                return
            
            zip_files = list(zip_path.glob("*.zip"))
            zip_files.sort()
            
            for zip_file in zip_files:
                self.file_listbox.insert(tk.END, zip_file.name)
            
            self.log_message(f"{len(zip_files)} ZIP-Dateien gefunden")
            
        except Exception as e:
            self.log_message(f"Fehler beim Laden der ZIP-Dateien: {e}")
    
    def select_all_files(self):
        """Wähle alle Dateien aus"""
        self.file_listbox.selection_set(0, tk.END)
    
    def deselect_all_files(self):
        """Hebe Auswahl aller Dateien auf"""
        self.file_listbox.selection_clear(0, tk.END)
    
    def install_selected_mods(self):
        """Installiere ausgewählte Mods"""
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie mindestens eine ZIP-Datei aus.")
            return
        
        if not self.current_version.get() or "Nicht gefunden" in self.current_version.get() or "Fehler" in self.current_version.get():
            messagebox.showerror("Version Fehler", "Keine gültige World of Tanks Version erkannt. Bitte überprüfen Sie den Installationspfad.")
            return
        
        # Starte Installation in separatem Thread
        threading.Thread(target=self._install_mods_thread, args=(selected_indices,), daemon=True).start()
    
    def _install_mods_thread(self, selected_indices):
        """Installation im separaten Thread"""
        try:
            self.progress.start()
            self.log_message("=== Installation gestartet ===")
            
            current_version = self.current_version.get()
            wot_base_path = Path(self.wot_path.get())  # Direkt in den WoT Hauptordner
            zip_path = Path(self.zip_folder.get())
            
            success_count = 0
            error_count = 0
            
            for index in selected_indices:
                zip_filename = self.file_listbox.get(index)
                zip_file_path = zip_path / zip_filename
                
                try:
                    self.log_message(f"Installiere: {zip_filename}")
                    
                    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                        for member in zip_ref.namelist():
                            # Überspringe Ordner
                            if member.endswith('/') or member.endswith('\\'):
                                continue
                            
                            # Intelligente Versionserkennung und -ersetzung
                            target_path = self.smart_version_replacement(member, current_version)
                            
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
                                self.log_message(f"  {member} → {target_path}")
                            else:
                                self.log_message(f"  → {target_path}")
                    
                    success_count += 1
                    self.log_message(f"✓ {zip_filename} erfolgreich installiert")
                    
                except Exception as e:
                    error_count += 1
                    self.log_message(f"✗ Fehler bei {zip_filename}: {e}")
            
            self.log_message(f"=== Installation abgeschlossen ===")
            self.log_message(f"Erfolgreich: {success_count}, Fehler: {error_count}")
            
            if error_count == 0:
                self.root.after(0, lambda: messagebox.showinfo("Installation abgeschlossen", 
                    f"Alle {success_count} Mods wurden erfolgreich installiert!"))
            else:
                self.root.after(0, lambda: messagebox.showwarning("Installation abgeschlossen", 
                    f"Installation abgeschlossen.\nErfolgreich: {success_count}\nFehler: {error_count}\n\nBitte prüfen Sie das Log für Details."))
                    
        except Exception as e:
            self.log_message(f"Kritischer Fehler: {e}")
            self.root.after(0, lambda: messagebox.showerror("Installation Fehler", f"Kritischer Fehler bei der Installation:\n{e}"))
        
        finally:
            self.progress.stop()
    
    def preview_selected_mods(self):
        """Zeige Vorschau für ausgewählte Mods"""
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie mindestens eine ZIP-Datei aus.")
            return
        
        if not self.current_version.get() or "Nicht gefunden" in self.current_version.get() or "Fehler" in self.current_version.get():
            messagebox.showerror("Version Fehler", "Keine gültige World of Tanks Version erkannt. Bitte überprüfen Sie den Installationspfad.")
            return
        
        # Sammle Preview-Daten
        preview_data = []
        current_version = self.current_version.get()
        wot_base_path = Path(self.wot_path.get())
        zip_path = Path(self.zip_folder.get())
        
        for index in selected_indices:
            zip_filename = self.file_listbox.get(index)
            zip_file_path = zip_path / zip_filename
            
            try:
                file_data = {"name": zip_filename, "files": []}
                
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    for member in zip_ref.namelist():
                        if member.endswith('/') or member.endswith('\\'):
                            continue  # Überspringe Ordner
                            
                        # Alle Dateien werden kopiert, aber "version" wird durch aktuelle Spielversion ersetzt
                        if "/version/" in member or "\\version\\" in member:
                            # Ersetze "version" durch aktuelle Spielversion
                            target_path = member.replace("/version/", f"/{current_version}/").replace("\\version\\", f"\\{current_version}\\")
                            file_data["files"].append({"source": member, "target": target_path})
                        else:
                            # Normale Datei - wird direkt kopiert (res/, mods/configs/, res_mods/, etc.)
                            file_data["files"].append({"source": member, "target": member})
                
                preview_data.append(file_data)
                
            except Exception as e:
                file_data = {"name": zip_filename, "error": str(e), "files": []}
                preview_data.append(file_data)
        
        # Zeige Preview-Dialog
        self.show_preview_dialog(preview_data)
    
    def show_preview_dialog(self, preview_data):
        """Zeige Preview-Dialog mit den Installationsinformationen"""
        # Erstelle neues Fenster
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Installations-Vorschau")
        preview_window.geometry("800x600")
        preview_window.resizable(True, True)
        
        # Hauptframe
        main_frame = ttk.Frame(preview_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Info-Label
        info_label = ttk.Label(main_frame, 
            text=f"Vorschau für {len(preview_data)} ausgewählte ZIP-Datei(en):",
            font=("Arial", 10, "bold"))
        info_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Scrollbarer Textbereich
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        preview_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Consolas", 9))
        preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Fülle Textbereich mit Preview-Daten
        for file_data in preview_data:
            preview_text.insert(tk.END, f"\n{'=' * 60}\n")
            preview_text.insert(tk.END, f"ZIP-Datei: {file_data['name']}\n")
            preview_text.insert(tk.END, f"{'=' * 60}\n")
            
            if "error" in file_data:
                preview_text.insert(tk.END, f"FEHLER: {file_data['error']}\n")
            else:
                if len(file_data['files']) == 0:
                    preview_text.insert(tk.END, "Keine installierbaren Dateien gefunden.\n")
                else:
                    preview_text.insert(tk.END, f"Zu installierende Dateien ({len(file_data['files'])}):\n\n")
                    
                    for file_info in file_data['files']:
                        if file_info['source'] != file_info['target']:
                            preview_text.insert(tk.END, f"  {file_info['source']}\n")
                            preview_text.insert(tk.END, f"  → {file_info['target']}\n\n")
                        else:
                            preview_text.insert(tk.END, f"  {file_info['target']}\n\n")
            
            preview_text.insert(tk.END, "\n")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Schließen", 
                  command=preview_window.destroy).pack(side=tk.RIGHT)
        
        ttk.Button(button_frame, text="Jetzt installieren", 
                  command=lambda: [preview_window.destroy(), self.install_selected_mods()]).pack(side=tk.RIGHT, padx=(0, 10))
        
        # Zentriere das Fenster
        preview_window.transient(self.root)
        preview_window.grab_set()

    def run(self):
        """Starte die Anwendung"""
        self.root.mainloop()


if __name__ == "__main__":
    app = WoTModInstaller()
    app.run()