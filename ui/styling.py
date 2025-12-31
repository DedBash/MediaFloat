from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette

COLOR_WINDOW = QColor(53, 53, 53)
COLOR_WINDOW_TEXT = Qt.GlobalColor.white
COLOR_BASE = QColor(25, 25, 25)
COLOR_ALT_BASE = QColor(53, 53, 53)
COLOR_TOOLTIP_BASE = Qt.GlobalColor.white
COLOR_TOOLTIP_TEXT = Qt.GlobalColor.white
COLOR_TEXT = Qt.GlobalColor.white
COLOR_BUTTON = QColor(80, 80, 80)
COLOR_BUTTON_TEXT = Qt.GlobalColor.white
COLOR_BRIGHT_TEXT = Qt.GlobalColor.red
COLOR_LINK = QColor(42, 130, 218)
COLOR_HIGHLIGHT = QColor(42, 130, 218)
COLOR_HIGHLIGHTED_TEXT = Qt.GlobalColor.black


def build_dark_palette() -> QPalette:
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, COLOR_WINDOW)
    palette.setColor(QPalette.ColorRole.WindowText, COLOR_WINDOW_TEXT)
    palette.setColor(QPalette.ColorRole.Base, COLOR_BASE)
    palette.setColor(QPalette.ColorRole.AlternateBase, COLOR_ALT_BASE)
    palette.setColor(QPalette.ColorRole.ToolTipBase, COLOR_TOOLTIP_BASE)
    palette.setColor(QPalette.ColorRole.ToolTipText, COLOR_TOOLTIP_TEXT)
    palette.setColor(QPalette.ColorRole.Text, COLOR_TEXT)
    palette.setColor(QPalette.ColorRole.Button, COLOR_BUTTON)
    palette.setColor(QPalette.ColorRole.ButtonText, COLOR_BUTTON_TEXT)
    palette.setColor(QPalette.ColorRole.BrightText, COLOR_BRIGHT_TEXT)
    palette.setColor(QPalette.ColorRole.Link, COLOR_LINK)
    palette.setColor(QPalette.ColorRole.Highlight, COLOR_HIGHLIGHT)
    palette.setColor(QPalette.ColorRole.HighlightedText, COLOR_HIGHLIGHTED_TEXT)
    return palette

def apply_dark_theme(app) -> None:
    app.setStyle("Fusion")
    app.setPalette(build_dark_palette())

def qss_flyout_container() -> str:
    return """
        QFrame {
            background-color: rgba(32, 32, 32, 220);
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 28);
        }
        QLabel { color: white; }
    """


def qss_flyout_info_card() -> str:
    return """
        QFrame {
            background-color: rgba(255, 255, 255, 10);
            border: 1px solid rgba(255, 255, 255, 12);
            border-radius: 12px;
        }
    """


def qss_flyout_chip_button() -> str:
    return """
        QPushButton {
            background-color: rgba(255, 255, 255, 12);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 16);
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 18);
            border: 1px solid rgba(255, 255, 255, 28);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 8);
        }
    """


def qss_flyout_media_button() -> str:
    return """
        QPushButton {
            background-color: rgba(255, 255, 255, 20);
            border-radius: 26px;
            border: 1px solid rgba(255, 255, 255, 30);
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 40);
            border: 1px solid rgba(255, 255, 255, 80);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 10);
        }
    """


def qss_flyout_combo() -> str:
    return """
        QComboBox {
            background-color: rgba(60, 60, 60, 180);
            color: white;
            border: 1px solid rgba(255, 255, 255, 25);
            padding: 6px 10px;
            border-radius: 14px;
            min-height: 28px;
            font-size: 12px;
        }
        QComboBox:hover {
            background-color: rgba(80, 80, 80, 190);
            border: 1px solid rgba(255, 255, 255, 40);
        }
        QComboBox::drop-down {
            border: none;
            width: 28px;
            border-top-right-radius: 14px;
            border-bottom-right-radius: 14px;
        }
        QComboBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 6px solid #ddd;
            margin-right: 10px;
        }
        QComboBox QAbstractItemView {
            background-color: #2b2b2b;
            color: white;
            selection-background-color: #444;
            selection-color: white;
            border: 1px solid #555;
            border-radius: 8px;
            outline: none;
        }
        QComboBox::item {
            height: 32px;
            padding-left: 8px;
        }
        QComboBox::item:selected {
            background-color: #444;
        }
    """
