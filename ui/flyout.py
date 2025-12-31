from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QFrame, QStyle, QComboBox)
from PyQt6.QtCore import Qt, QSize
from .icons import get_white_icon, get_gear_icon, get_close_icon, get_session_app_icon
from utils.helpers import get_text, DEFAULT_LANGUAGE
from .styling import (
    qss_flyout_chip_button,
    qss_flyout_combo,
    qss_flyout_container,
    qss_flyout_info_card,
    qss_flyout_media_button,
)

class FlyoutWindow(QWidget):
    def __init__(self, media_worker, parent=None):
        super().__init__(parent)
        self.media_worker = media_worker
        self.current_session_id = None
        self.lang_code = DEFAULT_LANGUAGE
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.container = QFrame()
        self.container.setStyleSheet(qss_flyout_container())
        
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(12, 12, 12, 12)
        container_layout.setSpacing(10)

        self.info_frame = QFrame()
        self.info_frame.setStyleSheet(qss_flyout_info_card())
        info_layout = QVBoxLayout(self.info_frame)
        info_layout.setContentsMargins(12, 10, 12, 10)
        info_layout.setSpacing(4)

        self.label_title = QLabel("")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.label_title.setStyleSheet("font-weight: 650; font-size: 16px; color: rgba(255, 255, 255, 235);")
        self.label_title.setWordWrap(True)

        self.label_artist = QLabel("")
        self.label_artist.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.label_artist.setStyleSheet("font-size: 12px; color: rgba(255, 255, 255, 160);")
        self.label_artist.setWordWrap(True)

        info_layout.addWidget(self.label_title)
        info_layout.addWidget(self.label_artist)

        container_layout.addWidget(self.info_frame)
        
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(0, 4, 0, 0)
        controls_layout.setSpacing(12)
        self.btn_prev = QPushButton()
        self.btn_prev.setIcon(get_white_icon(QStyle.StandardPixmap.SP_MediaSkipBackward))
        self.btn_prev.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_play = QPushButton()
        self.btn_play.setIcon(get_white_icon(QStyle.StandardPixmap.SP_MediaPlay))
        self.btn_play.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_next = QPushButton()
        self.btn_next.setIcon(get_white_icon(QStyle.StandardPixmap.SP_MediaSkipForward))
        self.btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        
        for btn in [self.btn_prev, self.btn_play, self.btn_next]:
            btn.setFixedSize(52, 52)
            btn.setIconSize(QSize(24, 24))
            btn.setStyleSheet(qss_flyout_media_button())
        
        controls_layout.addWidget(self.btn_prev)
        controls_layout.addWidget(self.btn_play)
        controls_layout.addWidget(self.btn_next)
        
        self.btn_prev.clicked.connect(lambda: self.media_worker.perform_action("prev", self.current_session_id))
        self.btn_play.clicked.connect(lambda: self.media_worker.perform_action("play_pause", self.current_session_id))
        self.btn_next.clicked.connect(lambda: self.media_worker.perform_action("next", self.current_session_id))

        container_layout.addLayout(controls_layout)

        self.combo_sessions = QComboBox()
        self.combo_sessions.setCursor(Qt.CursorShape.PointingHandCursor)
        self.combo_sessions.setIconSize(QSize(18, 18))
        self.combo_sessions.setStyleSheet(qss_flyout_combo())
        self.combo_sessions.currentIndexChanged.connect(self.on_session_changed)
        self.combo_sessions.hide()
        container_layout.addWidget(self.combo_sessions)

        utils_layout = QHBoxLayout()
        utils_layout.setContentsMargins(0, 2, 0, 0)
        utils_layout.setSpacing(10)

        self.btn_settings = QPushButton()
        self.btn_settings.setIcon(get_gear_icon())
        self.btn_settings.setFixedSize(40, 40)
        self.btn_settings.setIconSize(QSize(18, 18))
        self.btn_settings.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_settings.setStyleSheet(qss_flyout_chip_button())

        self.btn_hide = QPushButton()
        self.btn_hide.setIcon(get_close_icon())
        self.btn_hide.setFixedSize(40, 40)
        self.btn_hide.setIconSize(QSize(18, 18))
        self.btn_hide.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_hide.setStyleSheet(self.btn_settings.styleSheet())

        utils_layout.addWidget(self.btn_settings)
        utils_layout.addStretch()
        utils_layout.addWidget(self.btn_hide)

        container_layout.addLayout(utils_layout)
        
        self.layout.addWidget(self.container)
        self.resize(280, 250)
        
        self.media_worker.media_sessions_changed.connect(self.update_media_sessions)

        self.update_texts()

    def set_language(self, lang_code):
        if lang_code:
            self.lang_code = lang_code
            self.update_texts()

    def update_texts(self):
        self.btn_settings.setToolTip(get_text("flyout_settings_tooltip", self.lang_code))
        self.btn_hide.setToolTip(get_text("flyout_hide_tooltip", self.lang_code))
        if not self.label_title.text():
            self.label_title.setText(get_text("no_media", self.lang_code))

    def on_session_changed(self, index):
        if index >= 0:
            self.current_session_id = self.combo_sessions.itemData(index)

    def update_media_sessions(self, sessions):
        if not self.isVisible():
            return
            
        current_ids = [s['id'] for s in sessions]
        combo_ids = [self.combo_sessions.itemData(i) for i in range(self.combo_sessions.count())]
        
        if combo_ids != current_ids:
            self.combo_sessions.blockSignals(True)
            self.combo_sessions.clear()
            for s in sessions:
                display_name = s['id']
                if "!" in display_name:
                    display_name = display_name.split("!")[-1]
                
                icon = get_session_app_icon(s['id'])
                
                self.combo_sessions.addItem(icon, display_name, s['id'])
            
            index = self.combo_sessions.findData(self.current_session_id)
            if index >= 0:
                self.combo_sessions.setCurrentIndex(index)
            elif self.combo_sessions.count() > 0:
                self.combo_sessions.setCurrentIndex(0)
                self.current_session_id = self.combo_sessions.itemData(0)
            else:
                self.current_session_id = None
            
            self.combo_sessions.blockSignals(False)

        if len(sessions) > 1:
            self.combo_sessions.show()
        else:
            self.combo_sessions.hide()

        selected_session = next((s for s in sessions if s['id'] == self.current_session_id), None)
        
        if not selected_session and sessions:
            selected_session = sessions[0]
            self.current_session_id = selected_session['id']
            
        if selected_session:
            self.update_ui_with_session(selected_session)
        else:
            self.update_ui_no_media()

    def update_ui_with_session(self, info):
        title = info.get("title", "")
        artist = info.get("artist", "")
        
        if len(title) > 30: title = title[:27] + "..."
        if len(artist) > 30: artist = artist[:27] + "..."
        
        self.label_title.setText(title if title else get_text("unknown_title", self.lang_code))
        if artist:
            self.label_artist.setText(artist)
            self.label_artist.show()
        else:
            self.label_artist.setText("")
            self.label_artist.hide()
        
        is_playing = info.get("is_playing", False)
        if is_playing:
            self.btn_play.setIcon(get_white_icon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.btn_play.setIcon(get_white_icon(QStyle.StandardPixmap.SP_MediaPlay))

    def update_ui_no_media(self):
        self.label_title.setText(get_text("no_media", self.lang_code))
        self.label_artist.setText("")
        self.label_artist.hide()
        self.btn_play.setIcon(get_white_icon(QStyle.StandardPixmap.SP_MediaPlay))

    def leaveEvent(self, event):
        super().leaveEvent(event)
