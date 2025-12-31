from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QStyle)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from .icons import get_white_pixmap

class FloatingBar(QWidget):
    def __init__(self, flyout_window):
        super().__init__()
        self.flyout = flyout_window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        
        self.current_size = 30
        self.resize(self.current_size, self.current_size)
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 40, screen.height() // 2)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.arrow_lbl = QLabel()
        self.arrow_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.arrow_lbl.setCursor(Qt.CursorShape.PointingHandCursor)
        self.arrow_lbl.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.arrow_lbl.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        
        self.bg_color = QColor(0, 0, 0, 100)
        self.border_radius = 15
        self.update_style()
        
        layout.addWidget(self.arrow_lbl)
        
        self.old_pos = None
        self.is_dragging = False
        self.edge = 'right'

    def update_style(self, color=None, size=None, radius=None):
        if color: self.bg_color = color
        if size: 
            self.current_size = size
            self.resize(size, size)
        if radius is not None: self.border_radius = radius
            
        r, g, b, a = self.bg_color.red(), self.bg_color.green(), self.bg_color.blue(), self.bg_color.alpha()
        
        style = f"""
            QLabel {{
                background-color: rgba({r}, {g}, {b}, {a});
                border-radius: {self.border_radius}px;
                border: 1px solid rgba(255, 255, 255, 30);
            }}
            QLabel:hover {{
                background-color: rgba({r}, {g}, {b}, {min(255, a + 50)});
                border: 1px solid rgba(255, 255, 255, 100);
            }}
        """
        self.arrow_lbl.setStyleSheet(style)
        self.snap_to_edge()

    def enterEvent(self, event):
        super().enterEvent(event)

    def show_flyout(self):
        bar_geo = self.geometry()
        flyout_width = self.flyout.width()
        flyout_height = self.flyout.height()
        
        if self.edge == 'right':
            x = bar_geo.x() - flyout_width - 5
            y = bar_geo.y() + (bar_geo.height() - flyout_height) // 2
        elif self.edge == 'left':
            x = bar_geo.right() + 5
            y = bar_geo.y() + (bar_geo.height() - flyout_height) // 2
        elif self.edge == 'top':
            x = bar_geo.x() + (bar_geo.width() - flyout_width) // 2
            y = bar_geo.bottom() + 5
        else:
            x = bar_geo.x() + (bar_geo.width() - flyout_width) // 2
            y = bar_geo.y() - flyout_height - 5
        
        self.flyout.move(x, y)
        self.flyout.show()
        self.flyout.raise_()

    def toggle_flyout(self):
        if self.flyout.isVisible():
            self.flyout.hide()
        else:
            self.show_flyout()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()
            self.is_dragging = False

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            if (delta.manhattanLength() > 5) or self.is_dragging:
                self.is_dragging = True
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.old_pos = event.globalPosition().toPoint()
                self.flyout.hide()

    def mouseReleaseEvent(self, event):
        if self.is_dragging:
            self.snap_to_edge()
        elif event.button() == Qt.MouseButton.LeftButton:
            self.toggle_flyout()
            
        self.old_pos = None
        self.is_dragging = False

    def snap_to_edge(self):
        screen = QApplication.primaryScreen().geometry()
        pos = self.geometry().center()
        
        dist_left = pos.x() - screen.left()
        dist_right = screen.right() - pos.x()
        dist_top = pos.y() - screen.top()
        dist_bottom = screen.bottom() - pos.y()
        
        min_dist = min(dist_left, dist_right, dist_top, dist_bottom)
        
        new_x = self.x()
        new_y = self.y()
        
        if min_dist == dist_left:
            new_x = screen.left()
            self.edge = 'left'
            self.arrow_lbl.setPixmap(get_white_pixmap(QStyle.StandardPixmap.SP_ArrowRight, 16))
        elif min_dist == dist_right:
            new_x = screen.right() - self.width()
            self.edge = 'right'
            self.arrow_lbl.setPixmap(get_white_pixmap(QStyle.StandardPixmap.SP_ArrowLeft, 16))
        elif min_dist == dist_top:
            new_y = screen.top()
            self.edge = 'top'
            self.arrow_lbl.setPixmap(get_white_pixmap(QStyle.StandardPixmap.SP_ArrowDown, 16))
        else:
            new_y = screen.bottom() - self.height()
            self.edge = 'bottom'
            self.arrow_lbl.setPixmap(get_white_pixmap(QStyle.StandardPixmap.SP_ArrowUp, 16))
            
        self.move(new_x, new_y)
