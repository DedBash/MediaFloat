import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.styling import apply_dark_theme
from ui.icons import get_app_icon
from core.media import MediaWorker

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(get_app_icon())
    
    apply_dark_theme(app)
    
    media_worker = MediaWorker()
    media_worker.start()
    
    window = MainWindow(media_worker)

    if getattr(window, "startup_ui_state", "window") == "window":
        window.show()
    
    exit_code = app.exec()
    
    media_worker.stop()
    
    sys.exit(exit_code)
