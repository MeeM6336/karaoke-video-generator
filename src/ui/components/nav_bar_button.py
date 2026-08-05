from PySide6.QtWidgets import QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap

class NavBarButton(QPushButton):

	page_changed = Signal(int)

	def __init__(self, button_text, page_num, icon_path):
		super().__init__()

		self.page_num = page_num

		layout = QHBoxLayout(self) 
		layout.setSpacing(30) 
		layout.setAlignment(Qt.AlignLeft)

		self.setObjectName("NavButton")

		self.button_text_r = QLabel(button_text)

		self.button_text_l = QLabel(">") 
		self.button_text_r = QLabel(button_text) 
		self.button_icon = QLabel() 
		self.button_icon.setPixmap( 
			QPixmap(icon_path).scaled(
				22, 22,
				Qt.KeepAspectRatio, 
				Qt.SmoothTransformation 
			) 
		)

		layout.addWidget(self.button_text_l) 
		layout.addWidget(self.button_icon) 
		layout.addWidget(self.button_text_r)
		self.setCheckable(True)

		self.clicked.connect(lambda: self.page_changed.emit(self.page_num))

		self.setStyleSheet("""
				QPushButton#NavButton {
					background: transparent;
					border: none;
					text-align: left;
					padding: 30px 246px 30px 0px;
				}

				QPushButton#NavButton:hover {
					background: #2d2d2d;
				}

				QPushButton#NavButton:checked {
					background: #2d2d2d;
				}
				
				QLabel { 
					color: white; 
					font-size: 22px; 
					font-weight: normal; 
				}
		""")