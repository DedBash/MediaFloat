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
            background-color: rgba(35, 35, 35, 235);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 35);
        }
        QLabel { color: white; }
    """


def qss_flyout_info_card() -> str:
    return """
        QFrame {
            background-color: rgba(255, 255, 255, 13);
            border: 1px solid rgba(255, 255, 255, 18);
            border-radius: 12px;
        }
    """


def qss_flyout_chip_button() -> str:
    return """
        QPushButton {
            background-color: rgba(255, 255, 255, 14);
            border-radius: 22px;
            border: 1px solid rgba(255, 255, 255, 20);
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 24);
            border: 1px solid rgba(255, 255, 255, 40);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 10);
        }
    """


def qss_flyout_media_button() -> str:
    return """
        QPushButton {
            background-color: rgba(255, 255, 255, 24);
            border-radius: 28px;
            border: 1px solid rgba(255, 255, 255, 35);
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 45);
            border: 2px solid rgba(255, 255, 255, 90);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 15);
        }
    """


def qss_flyout_combo() -> str:
    return """
        QComboBox {
            background-color: rgba(255, 255, 255, 14);
            color: white;
            border: 1px solid rgba(255, 255, 255, 25);
            padding: 6px 28px 6px 40px;
            border-radius: 22px;
            min-height: 28px;
            font-size: 12px;
            font-weight: 500;
        }
        QComboBox:hover {
            background-color: rgba(255, 255, 255, 22);
            border: 1px solid rgba(255, 255, 255, 40);
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: center right;
            width: 24px;
            border: none;
        }
        QComboBox::down-arrow {
            image: none;
        }
        QComboBox QAbstractItemView {
            background-color: #2a2a2a;
            color: white;
            selection-background-color: #454545;
            selection-color: white;
            border: 1px solid rgba(255, 255, 255, 50);
            border-radius: 10px;
            outline: none;
            padding: 4px;
        }
        QComboBox::item {
            height: 32px;
            padding-left: 36px;
            border-radius: 6px;
            margin: 2px 4px;
        }
        QComboBox::item:hover {
            background-color: #353535;
        }
        QComboBox::item:selected {
            background-color: #454545;
        }
    """


def qss_combo_arrow_label() -> str:
    return """
        color: rgba(255, 255, 255, 180);
        font-size: 11px;
        background: transparent;
        border: none;
    """


def qss_main_window_label() -> str:
    return """
        font-size: 16px; 
        font-weight: 700;
        color: #e0e0e0;
        padding: 10px;
    """


def qss_main_window_button() -> str:
    return """
        QPushButton {
            background-color: rgba(80, 80, 80, 255);
            border: 1px solid rgba(255, 255, 255, 50);
            border-radius: 8px;
            padding: 10px;
            font-size: 13px;
        }
        QPushButton:hover {
            background-color: rgba(100, 100, 100, 255);
            border: 1px solid rgba(255, 255, 255, 100);
        }
        QPushButton:pressed {
            background-color: rgba(60, 60, 60, 255);
        }
    """


def qss_main_window_button_primary() -> str:
    return """
        QPushButton {
            background-color: rgba(42, 130, 218, 255);
            border: 1px solid rgba(255, 255, 255, 50);
            border-radius: 8px;
            padding: 10px;
            font-size: 13px;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: rgba(52, 140, 228, 255);
            border: 1px solid rgba(255, 255, 255, 100);
        }
        QPushButton:pressed {
            background-color: rgba(32, 120, 208, 255);
        }
    """


def qss_main_window_groupbox() -> str:
    return """
        QGroupBox {
            font-size: 14px;
            font-weight: 600;
            border: 2px solid rgba(255, 255, 255, 30);
            border-radius: 10px;
            margin-top: 10px;
            padding-top: 15px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 5px;
        }
    """


def qss_flyout_title_label() -> str:
    return """
        font-weight: 700; 
        font-size: 17px; 
        color: rgba(255, 255, 255, 245);
        padding: 2px 0px;
    """


def qss_flyout_artist_label() -> str:
    return """
        font-size: 13px; 
        color: rgba(255, 255, 255, 170);
        padding: 2px 0px;
    """


def qss_floating_bar_label(r: int, g: int, b: int, a: int, radius: int) -> str:
    return f"""
        QLabel {{
            background-color: rgba({r}, {g}, {b}, {a});
            border-radius: {radius}px;
            border: 1px solid rgba(255, 255, 255, 40);
        }}
        QLabel:hover {{
            background-color: rgba({r}, {g}, {b}, {min(255, a + 60)});
            border: 2px solid rgba(255, 255, 255, 120);
        }}
    """
