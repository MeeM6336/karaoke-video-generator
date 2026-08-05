from PySide6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel, QButtonGroup
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QPixmap
from src.ui.components.nav_bar_button import NavBarButton

class NavBar(QWidget):
    page_changed = Signal(int)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setObjectName("NavBar")
                
        self.setAttribute(Qt.WA_StyledBackground, True)

        nav_bar_style = """
            QWidget#NavBar {
                background-color: #1f1f1f;
            }

            QLabel {
                font-size: 22px;
                font-weight: bold;
            }
        """

        self.setStyleSheet(nav_bar_style)

        self.logo_layout = QHBoxLayout()
        self.logo_layout.setContentsMargins(35, 30, 80, 20)
        self.logo_label = QLabel()
        self.logo_label.setText("K. Karaoke")
        self.button_icon = QLabel()
        self.button_icon.setPixmap(
            QPixmap("data/assets/icons/logo.png").scaled(
                48, 48,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )
        self.logo_layout.addWidget(self.button_icon)
        self.logo_layout.addWidget(self.logo_label)

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        self.create_button = NavBarButton("Create", 0, "data/assets/icons/create.png")
        self.group.addButton(self.create_button)

        self.upload_button = NavBarButton("Upload", 1, "data/assets/icons/upload.png")
        self.group.addButton(self.upload_button)

        self.edit_button = NavBarButton("Edit", 2, "data/assets/icons/edit.png")
        self.group.addButton(self.edit_button)

        self.convert_button = NavBarButton("Convert", 3, "data/assets/icons/convert.png")
        self.group.addButton(self.convert_button)

        layout.addLayout(self.logo_layout)
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
