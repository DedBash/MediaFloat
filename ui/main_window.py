from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QSystemTrayIcon, QMenu, QStyle, 
                             QGroupBox, QFormLayout, QSpinBox,
                             QCheckBox, QComboBox)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QAction, QColor, QCursor

from version import __version__, __app_name__
from .flyout import FlyoutWindow
from .floating_bar import FloatingBar
from .icons import get_app_icon
from .styling import (
    qss_main_window_label,
    qss_main_window_button,
    qss_main_window_button_primary,
    qss_main_window_groupbox,
)
from utils.helpers import TRANSLATIONS, DEFAULT_LANGUAGE, get_text, is_autostart_enabled, toggle_autostart

class MainWindow(QMainWindow):
    def __init__(self, media_worker):
        super().__init__()
        self.current_language = DEFAULT_LANGUAGE
        self.media_worker = media_worker
        self.startup_ui_state = "window"
        
        self.flyout = FlyoutWindow(media_worker)
        self.floating_bar = FloatingBar(self.flyout)
        
        self.flyout.btn_settings.clicked.connect(self.show_normal)
        self.flyout.btn_hide.clicked.connect(self.hide_all_to_tray)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        
        self.label_main = QLabel()
        self.label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_main.setStyleSheet(qss_main_window_label())
        
        self.btn_minimize_tray = QPushButton()
        self.btn_minimize_tray.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_minimize_tray.clicked.connect(self.hide_to_tray)
        self.btn_minimize_tray.setMinimumHeight(40)
        self.btn_minimize_tray.setStyleSheet(qss_main_window_button())
        
        self.btn_floating_mode = QPushButton()
        self.btn_floating_mode.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_floating_mode.clicked.connect(self.activate_floating_mode)
        self.btn_floating_mode.setMinimumHeight(40)
        self.btn_floating_mode.setStyleSheet(qss_main_window_button_primary())
        
        layout.addWidget(self.label_main)
        layout.addSpacing(5)
        layout.addWidget(self.btn_floating_mode)
        layout.addWidget(self.btn_minimize_tray)
        layout.addSpacing(10)
        
        self.settings_group = QGroupBox()
        self.settings_group.setStyleSheet(qss_main_window_groupbox())
        self.settings_layout = QFormLayout()
        self.settings_layout.setVerticalSpacing(12)
        self.settings_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.combo_language = QComboBox()
        self.combo_language.setCursor(Qt.CursorShape.PointingHandCursor)
        self.combo_language.setMinimumHeight(32)
        for lang_code, lang_data in TRANSLATIONS.items():
            display_name = lang_data.get("display_name", lang_code)
            self.combo_language.addItem(display_name, lang_code)
        self.combo_language.currentIndexChanged.connect(self.change_language)
        self.settings_layout.addRow("Sprache:", self.combo_language)

        self.spin_size = QSpinBox()
        self.spin_size.setRange(20, 100)
        self.spin_size.setValue(30)
        self.spin_size.setSuffix(" px")
        self.spin_size.setMinimumHeight(32)
        self.spin_size.valueChanged.connect(lambda v: self.floating_bar.update_style(size=v))
        self.settings_layout.addRow("Widget-Größe:", self.spin_size)
        
        self.check_autostart = QCheckBox()
        self.check_autostart.setCursor(Qt.CursorShape.PointingHandCursor)
        self.check_autostart.setChecked(self.is_autostart_enabled())
        self.check_autostart.stateChanged.connect(self.toggle_autostart)
        self.settings_layout.addRow("Mit Windows starten:", self.check_autostart)
        
        self.check_tray_notification = QCheckBox()
        self.check_tray_notification.setCursor(Qt.CursorShape.PointingHandCursor)
        self.check_tray_notification.setChecked(False)
        self.check_tray_notification.stateChanged.connect(self.save_settings)
        self.settings_layout.addRow("Tray-Benachrichtigung:", self.check_tray_notification)
        
        self.combo_tray_action = QComboBox()
        self.combo_tray_action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.combo_tray_action.setMinimumHeight(32)
        self.combo_tray_action.addItem("", "window")
        self.combo_tray_action.addItem("", "flyout")
        self.combo_tray_action.addItem("", "floating")
        self.combo_tray_action.currentIndexChanged.connect(self.save_settings)
        self.settings_layout.addRow("", self.combo_tray_action)
        
        self.settings_group.setLayout(self.settings_layout)
        layout.addWidget(self.settings_group)
        
        # Version Label
        self.label_version = QLabel(f"{__app_name__} v{__version__}")
        self.label_version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_version.setStyleSheet("""
            font-size: 11px;
            color: rgba(255, 255, 255, 100);
            padding: 5px;
        """)
        layout.addStretch()
        layout.addWidget(self.label_version)
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(get_app_icon())
        
        self.tray_menu = QMenu()
        self.action_show = QAction(self)
        self.action_show.triggered.connect(self.show_normal)
        
        self.action_quit = QAction(self)
        self.action_quit.triggered.connect(self.quit_app)
        
        self.tray_menu.addAction(self.action_show)
        self.tray_menu.addAction(self.action_quit)
        
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()
        
        self.load_settings()

    def hide_to_tray(self, show_message: bool = True):
        self.save_settings(ui_state="tray")
        self.flyout.hide()
        self.floating_bar.hide()
        self.hide()
        if show_message and self.check_tray_notification.isChecked():
            self.tray_icon.showMessage(
                get_text("tray_info_title", self.current_language),
                get_text("tray_info_msg", self.current_language),
            )

    def change_language(self, index):
        lang_code = self.combo_language.itemData(index)
        if lang_code:
            self.current_language = lang_code
            self.update_texts()
            self.save_settings()

    def update_texts(self):
        lang = self.current_language
        self.setWindowTitle(get_text("window_title", lang))
        self.label_main.setText(get_text("main_label", lang))
        self.btn_minimize_tray.setText(get_text("btn_minimize", lang))
        self.btn_floating_mode.setText(get_text("btn_floating", lang))
        self.settings_group.setTitle(get_text("group_settings", lang))
        
        # Tooltips setzen
        self.combo_language.setToolTip(get_text("tooltip_language", lang))
        self.spin_size.setToolTip(get_text("tooltip_widget_size", lang))
        self.check_autostart.setToolTip(get_text("tooltip_autostart", lang))
        self.check_tray_notification.setToolTip(get_text("tooltip_tray_notification", lang))
        self.combo_tray_action.setToolTip(get_text("tooltip_tray_action", lang))
        
        if self.settings_layout.labelForField(self.combo_language):
            self.settings_layout.labelForField(self.combo_language).setText(get_text("label_language", lang))
            
        if self.settings_layout.labelForField(self.spin_size):
            self.settings_layout.labelForField(self.spin_size).setText(get_text("label_size", lang))
            
        if self.settings_layout.labelForField(self.check_autostart):
            self.settings_layout.labelForField(self.check_autostart).setText(get_text("label_autostart", lang))
        
        if self.settings_layout.labelForField(self.check_tray_notification):
            self.settings_layout.labelForField(self.check_tray_notification).setText(get_text("label_tray_notification", lang))
        
        if self.settings_layout.labelForField(self.combo_tray_action):
            self.settings_layout.labelForField(self.combo_tray_action).setText(get_text("label_tray_click", lang))
        
        self.combo_tray_action.setItemText(0, get_text("tray_action_window", lang))
        self.combo_tray_action.setItemText(1, get_text("tray_action_flyout", lang))
        self.combo_tray_action.setItemText(2, get_text("tray_action_floating", lang))
        
        self.action_show.setText(get_text("tray_show", lang))
        self.action_quit.setText(get_text("tray_quit", lang))
        self.flyout.set_language(lang)
        self.floating_bar.set_language(lang)

    def quit_app(self):
        self.save_settings()
        QApplication.instance().quit()

    def is_autostart_enabled(self):
        return is_autostart_enabled()

    def toggle_autostart(self, state):
        toggle_autostart(state == 2)

    def load_settings(self):
        settings = QSettings("MediaFloat", "App")
        
        lang_code = settings.value("language", DEFAULT_LANGUAGE)
        index = self.combo_language.findData(lang_code)
        if index >= 0:
            self.combo_language.setCurrentIndex(index)
        self.current_language = lang_code
        self.update_texts()
        
        size = settings.value("widget_size", 30, type=int)
        self.spin_size.setValue(size)

        fixed_rgb = QColor(0, 0, 0, 100)
        self.floating_bar.update_style(color=fixed_rgb, size=size)
        
        tray_action = settings.value("tray_click_action", "window")
        index = self.combo_tray_action.findData(tray_action)
        if index >= 0:
            self.combo_tray_action.setCurrentIndex(index)
        
        show_tray_notification = settings.value("show_tray_notification", False, type=bool)
        self.check_tray_notification.setChecked(show_tray_notification)
        
        ui_state = settings.value("ui_state", "")
        if not ui_state:
            mode = settings.value("mode", "normal")
            ui_state = "floating" if mode == "floating" else "window"

        ui_state = str(ui_state)
        if ui_state not in {"window", "tray", "floating"}:
            ui_state = "window"

        self.startup_ui_state = ui_state
        if ui_state == "floating":
            self.activate_floating_mode(save=False)
        elif ui_state == "tray":
            # Nichts anzeigen, Tray-Icon bleibt aktiv
            self.flyout.hide()
            self.floating_bar.hide()
            self.hide()

    def save_settings(self, ui_state: str | None = None):
        settings = QSettings("MediaFloat", "App")
        settings.setValue("language", self.current_language)
        settings.setValue("widget_size", self.spin_size.value())
        
        tray_action = self.combo_tray_action.currentData()
        if tray_action:
            settings.setValue("tray_click_action", tray_action)
        
        settings.setValue("show_tray_notification", self.check_tray_notification.isChecked())

        if ui_state is None:
            if self.floating_bar.isVisible():
                ui_state = "floating"
            elif self.isVisible():
                ui_state = "window"
            else:
                ui_state = "tray"

        settings.setValue("ui_state", ui_state)
        settings.setValue("mode", "floating" if ui_state == "floating" else "normal")

    def activate_floating_mode(self, save: bool = True):
        if save:
            self.save_settings(ui_state="floating")
        self.hide()
        self.floating_bar.show()
        self.floating_bar.snap_to_edge()

    def hide_all_to_tray(self):
        self.hide_to_tray(show_message=True)

    def show_normal(self):
        self.save_settings(ui_state="window")
        self.floating_bar.hide()
        self.flyout.hide()
        self.show()
        self.raise_()
        self.activateWindow()

    def on_tray_icon_activated(self, reason):
        if reason in (QSystemTrayIcon.ActivationReason.Trigger, 
                      QSystemTrayIcon.ActivationReason.DoubleClick):
            settings = QSettings("MediaFloat", "App")
            action = settings.value("tray_click_action", "window")
            
            if action == "window":
                self.show_normal()
            elif action == "flyout":
                self.show_flyout_at_cursor()
            elif action == "floating":
                self.activate_floating_mode(save=True)
    def show_flyout_at_cursor(self):
        """Shows the flyout near the system tray / cursor."""
        self.floating_bar.hide()
        self.hide()
        
        # Position flyout near cursor/tray
        cursor_pos = QCursor.pos()
        screen = QApplication.primaryScreen().geometry()
        
        flyout_width = self.flyout.width()
        flyout_height = self.flyout.height()
        
        # Position near bottom-right (typical tray location)
        x = screen.right() - flyout_width - 10
        y = screen.bottom() - flyout_height - 50
        
        x = max(10, min(x, screen.right() - flyout_width - 10))
        y = max(10, min(y, screen.bottom() - flyout_height - 10))
        
        self.flyout.move(x, y)
        self.flyout.show()
        self.flyout.raise_()
        self.flyout.activateWindow()

    def changeEvent(self, event):
        if event.type() == event.Type.WindowStateChange:
            if self.windowState() & Qt.WindowState.WindowMinimized:
                event.ignore()
                self.hide_to_tray(show_message=True)
                return
        super().changeEvent(event)

    def closeEvent(self, event):
        event.ignore()
        self.hide_to_tray(show_message=False)
