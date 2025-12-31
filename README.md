# MediaFloat

**Version:** 0.2.0  
**Autor:** [DedBash](https://github.com/DedBash/MediaFloat)

Windows Media Controller mit Floating Widget

## Features
- Media-Steuerung über Windows SMTC
- Floating Widget am Bildschirmrand
- Flyout mit Medien-Infos
- Mehrsprachig (DE/EN/NL)
- Autostart
- Persistente Einstellungen

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
python main.py
```

## Build

```bash
build.bat
```

Oder manuell mit PyInstaller:

```bash
pyinstaller FloatControl.spec --noconfirm --clean
```

## Struktur

- `main.py` - Entry Point
- `ui/` - UI Komponenten (MainWindow, Flyout, FloatingBar)
- `core/` - Media Worker & SMTC Integration
- `utils/` - Übersetzungen, Autostart, Hilfsfunktionen
- `lang/` - JSON Sprachdateien

## Sprachen

Standard: Deutsch. Weitere Sprachen in `lang/` als JSON-Dateien.
