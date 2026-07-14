from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QProgressBar
from PySide6.QtCore import Signal

class TaskBar(QWidget):

    start_clicked = Signal(int)

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 200, 0, 0)

        self.setObjectName("TaskBarWidget")
        self.valid_start = False

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(
            lambda: self.start_clicked.emit(1) if self.valid_start else None
        )
        self.start_button.setEnabled(False)

        start_button_style = """
            QPushButton {
                background-color: #4a90e2;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 6px 15px;
                font-weight: bold;
            }

            QPushButton:disabled {
                background-color: #b0b0b0;
                color: #ffffff;
            }
        """
        
        self.setStyleSheet(start_button_style)

        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

    def set_valid_start(self, enabled: bool):
        self.valid_start = enabled
        self.start_button.setEnabled(enabled)
    
    def set_progress(self, progress):
        self.progress_bar.setValue(progress)
    