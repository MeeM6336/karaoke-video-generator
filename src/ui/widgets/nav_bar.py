from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, Signal


class NavBar(QWidget):

    page_changed = Signal(int)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Nav Bar Buttons
        nav_button_style = """
            QPushButton {
                background: transparent;
                border: none;
                padding: 12px 20px;
                color: white;
                font-size: 18px;
                height: 60px;
            }

            QPushButton:hover {
                background: #2d2d2d;
            }

            QPushButton:pressed {
                background: #1d1d1d;
            }
        """

        self.create_button = QPushButton("Create")
        self.create_button.setStyleSheet(nav_button_style)
        self.create_button.clicked.connect(
            lambda: self.page_changed.emit(0)
        )

        self.edit_button = QPushButton("Edit")
        self.edit_button.setStyleSheet(nav_button_style)
        self.edit_button.clicked.connect(
            lambda: self.page_changed.emit(1)
        )

        self.convert_button = QPushButton("Convert")
        self.convert_button.setStyleSheet(nav_button_style)
        self.convert_button.clicked.connect(
            lambda: self.page_changed.emit(2)
        )

        layout.addWidget(self.create_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.convert_button)
        
        self.setLayout(layout)
