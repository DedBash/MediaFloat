import os
import sys
from PyQt6.QtWidgets import QApplication, QFileIconProvider
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QBrush
from PyQt6.QtCore import Qt, QPoint, QFileInfo

try:
    import psutil
except Exception:
    psutil = None

def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)

def get_app_icon():
    path_png = resource_path(os.path.join("ui", "icons", "icon.png"))
    if os.path.exists(path_png):
        return QIcon(path_png)
        
    path_ico = resource_path(os.path.join("ui", "icons", "icon.ico"))
    if os.path.exists(path_ico):
        return QIcon(path_ico)
        
    return QIcon()

def get_process_path_by_id(app_id):
    if app_id.lower().endswith(".exe"):
        exe_name = app_id
        
        if os.path.exists(exe_name):
            return exe_name
            
        if psutil is None:
            return None

        for proc in psutil.process_iter(['name', 'exe']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == exe_name.lower():
                    return proc.info['exe']
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
    return None

def get_session_app_icon(app_id):
    path = get_process_path_by_id(app_id)
    
    if path and os.path.exists(path):
        provider = QFileIconProvider()
        icon = provider.icon(QFileInfo(path))
        if not icon.isNull():
            return icon
    
    # Fallback: Default Music Icon
    return get_default_music_icon()


def get_default_music_icon():
    """Gibt ein Standard-Musik-Icon zurück"""
    # Nutze Qt's Standard Media Play Icon als Fallback
    style = QApplication.style()
    if style:
        icon = style.standardIcon(style.StandardPixmap.SP_MediaPlay)
        if not icon.isNull():
            return icon
    
    # Wenn auch das fehlschlägt, erstelle ein einfaches Icon
    size = 32
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Einfacher Kreis mit Musiknote
    pen = painter.pen()
    pen.setColor(Qt.GlobalColor.white)
    pen.setWidth(2)
    painter.setPen(pen)
    painter.setBrush(QBrush(Qt.GlobalColor.transparent))
    
    # Äußerer Kreis
    painter.drawEllipse(4, 4, 24, 24)
    
    # Musiknote
    painter.setBrush(QBrush(Qt.GlobalColor.white))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(11, 18, 6, 6)
    painter.drawRect(16, 10, 2, 9)
    
    painter.end()
    return QIcon(pixmap)


def get_dropdown_arrow_icon(color=Qt.GlobalColor.white):
    """Erstellt ein einfaches Dropdown-Pfeil Icon"""
    size = 16
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen = painter.pen()
    pen.setColor(color)
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    
    # Pfeil nach unten zeichnen (V-Form)
    painter.drawLine(4, 6, 8, 10)
    painter.drawLine(8, 10, 12, 6)
    
    painter.end()
    return QIcon(pixmap)


def get_gear_icon(color=Qt.GlobalColor.white):
    size = 32
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    cx, cy = size / 2, size / 2
    
    painter.setBrush(QBrush(color))
    painter.setPen(Qt.PenStyle.NoPen)
    
    for i in range(8):
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(i * 45)
        painter.drawRect(-3, -14, 6, 8)
        painter.restore()
        
    painter.drawEllipse(QPoint(int(cx), int(cy)), 11, 11)
    
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
    painter.drawEllipse(QPoint(int(cx), int(cy)), 5, 5)
    
    painter.end()
    return QIcon(pixmap)


def get_close_icon(color=Qt.GlobalColor.white):
    size = 32
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen = painter.pen()
    pen.setColor(color)
    pen.setWidth(3)
    painter.setPen(pen)
    
    margin = 8
    painter.drawLine(margin, margin, size - margin, size - margin)
    painter.drawLine(size - margin, margin, margin, size - margin)
    
    painter.end()
    return QIcon(pixmap)

def get_white_icon(standard_pixmap):
    style = QApplication.style()
    icon = style.standardIcon(standard_pixmap)
    pixmap = icon.pixmap(32, 32)
    return QIcon(colorize_pixmap(pixmap, Qt.GlobalColor.white))

def get_white_pixmap(standard_pixmap, size=16):
    style = QApplication.style()
    icon = style.standardIcon(standard_pixmap)
    pixmap = icon.pixmap(size, size)
    return colorize_pixmap(pixmap, Qt.GlobalColor.white)


def colorize_pixmap(pixmap, color):
    if pixmap.isNull():
        return pixmap
        
    colored_pixmap = QPixmap(pixmap.size())
    colored_pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(colored_pixmap)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
    painter.drawPixmap(0, 0, pixmap)
    
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(colored_pixmap.rect(), color)
    painter.end()
    
    return colored_pixmap
