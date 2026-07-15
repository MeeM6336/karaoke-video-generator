from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout
from PySide6.QtCore import Qt
from ui.components.file_upload import FileUpload
from ui.components.task_bar import TaskBar


class Create(QWidget):

    def __init__(self):
        super().__init__()

        # Validation Flags
        self.valid_url = False

        self.setObjectName("CreateWidget")

        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.setSpacing(50)
        layout.setContentsMargins(50, 50, 50, 0)
        
        # Layout Style
        layout_style = """
            QWidget#CreateWidget {
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

        self.youtube_url = QLineEdit()
        self.youtube_url.setPlaceholderText("YouTube Video URL")
        self.youtube_url.textEdited.connect(self.validate_url)

        self.font_color = QLineEdit()
        self.font_color.setPlaceholderText("Font Color (e.g., #00FFFF)")

        self.filename = QLineEdit()
        self.filename.setPlaceholderText("Output Filename")

        self.song_lyric_query = QLineEdit()
        self.song_lyric_query.setPlaceholderText("Song name and artist to search for song lyrics")

        self.audio_upload = FileUpload("Audio", "Select an audio file", set_read_only=True)
        self.video_upload = FileUpload("Video", "Select a background video file", set_read_only=True)
        self.output_upload = FileUpload("Output", "Select a folder to output video", set_read_only=True)
        self.taskbar = TaskBar()

        layout.addWidget(self.youtube_url)
        layout.addWidget(self.audio_upload)
        layout.addWidget(self.video_upload)
        layout.addWidget(self.output_upload)
        layout.addWidget(self.filename)
        layout.addWidget(self.font_color)
        layout.addWidget(self.song_lyric_query)
        layout.addWidget(self.taskbar)

        self.setLayout(layout)

        self.audio_upload.path_changed.connect(self._on_path_changed)
        self.video_upload.path_changed.connect(self._on_path_changed)
        self.output_upload.path_changed.connect(self._on_path_changed)

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

    def _on_path_changed(self):
        self._update_valid_start()

    def _update_valid_start(self):
        if self.valid_url or (self.get_audio_path() and self.get_video_path()):
            self.taskbar.set_valid_start(True)
        
        else:
            self.taskbar.set_valid_start(False)

    def get_audio_path(self):
        return self.audio_upload.get_path()

    def get_video_path(self):
        return self.video_upload.get_path()

    def get_output_path(self):
        return self.output_upload.get_path()
    
    def get_job(self):
        return {
            "yt_link": self.youtube_url.text(),
            "audio_file": self.audio_upload.get_path(),
            "video_file": self.video_upload.get_path(),
            "output_dir": self.output_upload.get_path(),
            "filename": self.filename.text(),
            "font_color": self.font_color.text(),
            "query": self.song_lyric_query.text()
        }