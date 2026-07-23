from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout
from PySide6.QtGui import QIcon

class MissingDialog(QDialog):
    def __init__(self, messages):
        super().__init__()

        self.setWindowTitle("Missing Arguments")

        ok_btn = QDialogButtonBox.Ok

        self.resize(200, 150)

        self.setStyleSheet("""
            QDialog {
                background-color: #2b2a33;
            }

            QLabel {
                color: #ffffff;
            }

            QPushButton {
                background-color: #4a90e2;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 6px 15px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #5ba1f0;
            }

            QPushButton:pressed {
                    background-color: #3a7fcf;
            }
        """)

        self.setWindowIcon(QIcon("data/assets/icons/logo.png"))

        self.buttonBox = QDialogButtonBox(ok_btn)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        message = QLabel("Missing arguments:\n• " + "\n• ".join(messages))
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
