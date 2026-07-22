import sys
import ctypes

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QLoggingCategory
from src.ui.main_window import MainWindow


def run():
    myappid = "KaraokeVideoGenerator.1.0"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)

    QLoggingCategory.setFilterRules("""
        qt.multimedia.ffmpeg=false
    """)

    app.setWindowIcon(QIcon("data/assets/icons/logo.png"))

    window = MainWindow()
    window.setWindowIcon(QIcon("data/assets/icons/logo.png"))
    window.show()

    sys.exit(app.exec())