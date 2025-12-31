import json
import os
import sys
import winreg

def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)

DEFAULT_LANGUAGE = "de"
TRANSLATIONS = {}

def load_translations():
    global TRANSLATIONS
    lang_dir = resource_path("lang")
    
    if not os.path.exists(lang_dir):
        print(f"Language directory not found: {lang_dir}")
        return

    for filename in os.listdir(lang_dir):
        if filename.endswith(".json"):
            lang_code = filename.split(".")[0]
            try:
                with open(os.path.join(lang_dir, filename), "r", encoding="utf-8") as f:
                    TRANSLATIONS[lang_code] = json.load(f)
            except Exception as e:
                print(f"Error loading language {filename}: {e}")

load_translations()

def get_text(key, lang_code):
    lang_data = TRANSLATIONS.get(lang_code)
    if not lang_data:
        lang_data = TRANSLATIONS.get(DEFAULT_LANGUAGE, {})
    
    return lang_data.get(key, key)

def is_autostart_enabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
        try:
            winreg.QueryValueEx(key, "MediaFloat")
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            winreg.CloseKey(key)
            return False
    except Exception:
        return False

def toggle_autostart(state):
    try:
        if state:
            exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(sys.argv[0])
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "MediaFloat", 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
        else:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            try:
                winreg.DeleteValue(key, "MediaFloat")
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
    except Exception as e:
        print(f"Error toggling autostart: {e}")
