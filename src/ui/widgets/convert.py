from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QCheckBox
from PySide6.QtCore import Qt
from ui.components.task_bar import TaskBar


class Convert(QWidget):

    def __init__(self):
        super().__init__()

        self.valid_start = False

        self.setObjectName("ConvertWidget")
        
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Layout Style
        layout_style = """
            QWidget#ConvertWidget {
                background-color: #f0f0f0;
            }

            QLineEdit {
                padding: 5px;
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
        """
        self.setStyleSheet(layout_style)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)
        layout.setContentsMargins(50, 50, 50, 0)

        self.youtube_url = QLineEdit()
        self.youtube_url.setPlaceholderText("YouTube Video URL")
        self.youtube_url.textEdited.connect(self.validate_url)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.setAlignment(Qt.AlignLeft)
        checkbox_layout.setSpacing(20)
        checkbox_layout.setContentsMargins(10, 10, 50, 450)

        self.video_checkbox = QCheckBox()
        self.video_checkbox.setText("Download Video")

        self.audio_checkbox = QCheckBox()
        self.audio_checkbox.setText("Download Audio")

        self.task_bar = TaskBar()

        checkbox_layout.addWidget(self.video_checkbox)
        checkbox_layout.addWidget(self.audio_checkbox)

        layout.addWidget(self.youtube_url)
        layout.addLayout(checkbox_layout)
        layout.addWidget(self.task_bar)

        self.video_checkbox.toggled.connect(self._on_check_change)
        self.audio_checkbox.toggled.connect(self._on_check_change)

        self.setLayout(layout)
        

    def validate_url(self, text):
        valid_urls = (
            "https://youtu.be/",
            "https://www.youtube.com/",
            "www.youtube.com/",
            "www.youtu.be/",
            "youtu.be/",
            "youtube.com/"
        )

        self.valid_url = text.startswith(valid_urls)
        self._update_valid_start()

    def _on_check_change(self):
        self._update_valid_start()

    def _update_valid_start(self):
        if self.valid_url and (self.get_video_check() or self.get_audio_check()):
            self.task_bar.set_valid_start(True)
        
        else:
            self.task_bar.set_valid_start(False)
            
    def get_video_check(self):
        return self.video_checkbox.isChecked()

    def get_audio_check(self):
        return self.audio_checkbox.isChecked()

    def get_job(self):
        return {
            "yt_link": self.youtube_url.text(),
            "video": self.get_video_check(),
            "audio": self.get_audio_check()
        }

        
    