from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QCheckBox
from PySide6.QtCore import Qt


class Convert(QWidget):

    def __init__(self):
        super().__init__()

        self.valid_start = False

        self.setObjectName("ConvertWidget")
        
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout()

        self.youtube_url = QLineEdit()
        self.youtube_url.setPlaceholderText("YouTube Video URL")
        self.youtube_url.textEdited.connect(self.validate_url)

        checkbox_layout = QHBoxLayout()
        self.video_checkbox = QCheckBox()
        self.video_checkbox.setText("Download Video")

        checkbox_layout.addWidget(self.video_checkbox)

        layout.addWidget(self.youtube_url)
        layout.addLayout(checkbox_layout)

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
        self.valid_start = True



        
    