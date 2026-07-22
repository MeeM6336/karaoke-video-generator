from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QStackedLayout, QWidget
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

from src.ui.widgets.convert import Convert
from src.ui.widgets.nav_bar import NavBar
from src.ui.widgets.edit import Edit
from src.ui.widgets.create import Create
from src.ui.widgets.upload import Upload
from src.controller.main_controller import MainController


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kirk Karaoke Dashboard")
        self.setFixedSize(QSize(1440, 900))

        self.controller = MainController(self)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.stacked_layout = QStackedLayout()

        self.nav_bar = NavBar()
        self.nav_bar.page_changed.connect(
            self.controller.change_page
        )

        main_layout.addWidget(self.nav_bar, 1)
        main_layout.addLayout(self.stacked_layout, 4)

        self.create_widget = Create()
        self.create_widget.task_bar.start_clicked.connect(
            self.controller.start_karaoke_job
        )

        self.upload_widget = Upload()
        self.upload_widget.task_bar.start_clicked.connect(
            self.controller.start_upload_job
        )

        self.edit_widget = Edit()
        self.edit_widget.task_bar.start_clicked.connect(
            self.controller.start_edit_job
        )

        self.convert_widget = Convert()
        self.convert_widget.task_bar.start_clicked.connect(
            self.controller.start_convert_job
        )

        self.stacked_layout.addWidget(self.create_widget)
        self.stacked_layout.addWidget(self.upload_widget)
        self.stacked_layout.addWidget(self.edit_widget)
        self.stacked_layout.addWidget(self.convert_widget)

        self.stacked_layout.setCurrentIndex(0)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)