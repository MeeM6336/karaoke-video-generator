import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QLoggingCategory
from src.ui.main_window import MainWindow


def run():
    app = QApplication(sys.argv)

    QLoggingCategory.setFilterRules("""
        qt.multimedia.ffmpeg=false
    """)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())