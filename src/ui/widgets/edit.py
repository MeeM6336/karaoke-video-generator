from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class Edit(QWidget):
	def __init__(self):
		super().__init__()

		self.setObjectName("EditWidget")

		self.setAttribute(Qt.WA_StyledBackground, True)

		layout_style = """
			QWidget#EditWidget {
				background-color: #f0f0f0;
			}

			QLineEdit {
				padding: 10px;
				font-size: 14px;
				background-color: #ffffff;
				color: #000000;
			}
							
			QLineEdit:read-only {
				background-color: #f5f5f5;
				color: #000000;
			}
			
			QPushButton {
				background-color: #4a90e2;
				color: #ffffff;
				border: none;
				border-radius: 4px;
				padding: 6px 15px;
				font-weight: bold;
			}
			QLabel {
				font-size: 24px;
				color: #000000;
			}

		"""

		self.setStyleSheet(layout_style)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignCenter)

		self.wip_label = QLabel("Work in Progress")

		layout.addWidget(self.wip_label)

		self.setLayout(layout)
		
