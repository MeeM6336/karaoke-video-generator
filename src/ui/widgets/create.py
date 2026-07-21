from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout
from PySide6.QtCore import Qt
from src.ui.components.file_upload import FileUpload
from src.ui.components.task_bar import TaskBar


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
                background-color: #2b2a33;
            }

            QLineEdit {
                padding: 10px;
                font-size: 14px;
                color: #ffffff;
                background-color: #42414d;
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

            QPushButton:hover {
				background-color: #5ba1f0;
			}

			QPushButton:pressed {
				background-color: #3a7fcf;
			}
        """
        self.setStyleSheet(layout_style)

        self.youtube_url = QLineEdit()
        self.youtube_url.setPlaceholderText("YouTube Video URL")
        self.youtube_url.textEdited.connect(self.validate_url)
        self.youtube_url.setClearButtonEnabled(True)

        self.font_color = QLineEdit()
        self.font_color.setPlaceholderText("Font Color (e.g., #00FFFF)")
        self.font_color.setClearButtonEnabled(True)

        self.filename = QLineEdit()
        self.filename.setPlaceholderText("Output Filename")
        self.filename.setClearButtonEnabled(True)

        self.song_lyric_query = QLineEdit()
        self.song_lyric_query.setPlaceholderText("Song name and artist to search for song lyrics")
        self.song_lyric_query.setClearButtonEnabled(True)

        self.audio_upload = FileUpload("Audio", "Select an audio file")
        self.audio_upload.file_path.setClearButtonEnabled(True)
        self.video_upload = FileUpload("Video", "Select a background video file")
        self.video_upload.file_path.setClearButtonEnabled(True)
        self.output_upload = FileUpload("Output", "Select a folder to output video")
        self.output_upload.file_path.setClearButtonEnabled(True)

        self.task_bar = TaskBar()
        self.task_bar.setContentsMargins(0, 136, 0, 0)

        layout.addWidget(self.youtube_url)
        layout.addWidget(self.audio_upload)
        layout.addWidget(self.video_upload)
        layout.addWidget(self.output_upload)
        layout.addWidget(self.filename)
        layout.addWidget(self.font_color)
        layout.addWidget(self.song_lyric_query)
        layout.addWidget(self.task_bar)

        self.setLayout(layout)

        self.audio_upload.path_changed.connect(self._update_valid_start)
        self.video_upload.path_changed.connect(self._update_valid_start)
        self.output_upload.path_changed.connect(self._update_valid_start)

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


    def _update_valid_start(self):
        if self.valid_url or (self.get_audio_path() and self.get_video_path()):
            self.task_bar.set_valid_start(True)
        
        else:
            self.task_bar.set_valid_start(False)

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