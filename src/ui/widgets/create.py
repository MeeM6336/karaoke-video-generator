from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QColorDialog, QPushButton
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QColor, QIcon
from src.ui.components.file_upload import FileUpload
from src.ui.components.task_bar import TaskBar


class Create(QWidget):
    search_request = Signal(str)

    def __init__(self):
        super().__init__()

        self.lyrics = None

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
        self.youtube_url.setClearButtonEnabled(True)

        self.font_color = QLineEdit()
        self.font_color.setPlaceholderText("Font Color (e.g., #00FFFF)")
        self.font_color.setClearButtonEnabled(True)

        self.color_button = QPushButton()
        self.color_button.setIcon(QIcon("data/assets/icons/eyedropper.png"))
        self.color_button.setIconSize(QSize(16, 16))

        self.filename = QLineEdit()
        self.filename.setPlaceholderText("Output Filename")
        self.filename.setClearButtonEnabled(True)

        self.lyric_search_layout = QHBoxLayout()
        self.lyric_search_layout.setContentsMargins(0, 0, 0, 0)
        self.song_lyric_query = QLineEdit()
        self.song_lyric_query.setPlaceholderText("Song name and artist to search for song lyrics")
        self.song_lyric_query.setClearButtonEnabled(True)
        self.lyric_search_button = QPushButton()
        self.lyric_search_button.setIcon(QIcon("data/assets/icons/eyedropper.png"))
        self.lyric_search_button.setIconSize(QSize(16, 16))
        self.lyric_search_layout.addWidget(self.song_lyric_query)
        self.lyric_search_layout.addWidget(self.lyric_search_button)
        self.lyric_search_button.clicked.connect(lambda: self.search_request.emit(self.song_lyric_query.text().strip()))

        self.audio_upload = FileUpload("Audio", "Select an audio file")
        self.audio_upload.file_path.setClearButtonEnabled(True)
        self.video_upload = FileUpload("Video", "Select a background video file")
        self.video_upload.file_path.setClearButtonEnabled(True)  
        self.output_upload = FileUpload("Output", "Select a folder to output video")
        self.output_upload.file_path.setClearButtonEnabled(True)

        self.font_color_layout = QHBoxLayout()
        self.font_color_layout.setContentsMargins(0, 0, 0, 0)
        self.font_color_layout.addWidget(self.font_color)
        self.font_color_layout.addWidget(self.color_button)
        self.color_button.clicked.connect(self.pick_font_color)

        self.task_bar = TaskBar()
        self.task_bar.setContentsMargins(0, 136, 0, 0)

        layout.addWidget(self.youtube_url)
        layout.addWidget(self.audio_upload)
        layout.addWidget(self.video_upload)
        layout.addWidget(self.output_upload)
        layout.addWidget(self.filename)
        layout.addLayout(self.font_color_layout)
        layout.addLayout(self.lyric_search_layout)
        layout.addWidget(self.task_bar)

        self.setLayout(layout)


    def get_yt_link(self):
        return self.youtube_url.text()


    def get_audio_path(self):
        return self.audio_upload.get_path()


    def get_video_path(self):
        return self.video_upload.get_path()


    def get_output_path(self):
        return self.output_upload.get_path()


    def get_filename(self):
        return self.filename.text()


    def get_font_color(self):
        return self.font_color.text()


    def get_lyrics(self):
        return self.lyrics

    def set_lyrics(self, lyrics):
        self.lyrics = lyrics


    def pick_font_color(self):
        current = QColor(self.font_color.text())

        color = QColorDialog.getColor(
            current if current.isValid() else QColor("#00FFFF"),
            self,
            "Choose Font Color"
        )

        if color.isValid():
            self.font_color.setText(color.name())

    
    def get_job(self):
        return {
            "yt_link": self.get_yt_link(),
            "audio_file": self.get_audio_path(),
            "video_file": self.get_video_path(),
            "output_dir": self.get_output_path(),
            "filename": self.get_filename(),
            "font_color": self.get_font_color(),
            "lyrics": self.get_lyrics()
        }