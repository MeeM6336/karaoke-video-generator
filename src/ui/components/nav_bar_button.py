from PySide6.QtWidgets import QHBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QFont

class NavBarButton(QWidget):

	page_changed = Signal(int)

	def __init__(self, button_text, page_num, icon_path):
		super().__init__()

		self.page_num = page_num

		layout = QHBoxLayout(self)
		layout.setContentsMargins(80, 20, 100, 20)
		layout.setSpacing(30)
		layout.setAlignment(Qt.AlignLeft)

		self.setObjectName("NavButton")

		self.setAttribute(Qt.WA_Hover, True)
		self.setAttribute(Qt.WA_StyledBackground, True)

		nav_button_style = """
            QWidget#NavButton {
                color: white;
                text-align: left;
            }

            QWidget#NavButton:hover {
                background: #2d2d2d;
            }

            QWidget#NavButton:pressed {
                background: #1d1d1d;
            }
        """

		self.setStyleSheet(nav_button_style)

		self.button_text = QLabel(button_text)
		self.button_text.setStyleSheet("color: white; font-size: 20px;")

		self.button_icon = QLabel()
		self.button_icon.setPixmap(
			QPixmap(icon_path).scaled(
				32, 32,
				Qt.KeepAspectRatio,
				Qt.SmoothTransformation
			)
		)

		layout.addWidget(self.button_icon)
		layout.addWidget(self.button_text)


	
	def mousePressEvent(self, event):
		self.page_changed.emit(self.page_num)
		super().mousePressEvent(event)
