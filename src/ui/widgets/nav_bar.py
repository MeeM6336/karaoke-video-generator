from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from src.ui.components.nav_bar_button import NavBarButton

class NavBar(QWidget):
    page_changed = Signal(int)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.setContentsMargins(0, 40, 0, 0)

        self.create_button = NavBarButton("Create", 0, "data/assets/icons/create.png")

        self.upload_button = NavBarButton("Upload", 1, "data/assets/icons/upload.png")

        self.edit_button = NavBarButton("Edit", 2, "data/assets/icons/edit.png")

        self.convert_button = NavBarButton("Convert", 3, "data/assets/icons/convert.png")

        layout.addWidget(self.create_button)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.convert_button)

        for button in (
            self.create_button,
            self.convert_button,
            self.edit_button,
            self.upload_button,
        ):
            button.page_changed.connect(self.page_changed)
        
        self.setLayout(layout)
