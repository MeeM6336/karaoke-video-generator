from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QCheckBox
from PySide6.QtCore import Qt
from src.ui.components.task_bar import TaskBar
from src.ui.components.file_upload import FileUpload


class Upload(QWidget):
    def __init__(self):
        super().__init__()

        self.valid_start = False

        self.setObjectName("UploadWidget")

        self.setAttribute(Qt.WA_StyledBackground, True)

        layout_style = """
            QWidget#UploadWidget {
                background-color: #2b2a33;
            }

            QLineEdit {
                padding: 10px;
                font-size: 14px;
                background-color: #42414d;
                color: #ffffff;
            }

            QCheckBox {
				color: #ffffff;
				font-size: 14px;
				spacing: 8px;
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

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(50)
        layout.setContentsMargins(50, 50, 50, 0)

        self.file_upload = FileUpload("Video", "Select a file to upload")
        self.file_upload.file_path.setClearButtonEnabled(True)

        self.title = QLineEdit()
        self.title.setPlaceholderText("Title")
        self.title.setClearButtonEnabled(True)

        self.tags = QLineEdit()
        self.tags.setPlaceholderText("Tags")
        self.tags.setClearButtonEnabled(True)

        self.artist = QLineEdit()
        self.artist.setPlaceholderText("Artist")
        self.artist.setClearButtonEnabled(True)

        self.song = QLineEdit()
        self.song.setPlaceholderText("Song")
        self.song.setClearButtonEnabled(True)

        self.thumbnail_check = QCheckBox()
        self.thumbnail_check.setText("Generate thumbnail for video")

        self.task_bar = TaskBar()
        self.task_bar.setContentsMargins(0, 227, 0, 0)


        layout.addWidget(self.file_upload)
        layout.addWidget(self.title)
        layout.addWidget(self.tags)
        layout.addWidget(self.artist)
        layout.addWidget(self.song)
        layout.addWidget(self.thumbnail_check)
        layout.addWidget(self.task_bar)

        self.file_upload.path_changed.connect(self._update_valid_start)
        self.title.textChanged.connect(self._update_valid_start)
        self.tags.textChanged.connect(self._update_valid_start)
        self.artist.textChanged.connect(self._update_valid_start)
        self.song.textChanged.connect(self._update_valid_start)

        self.setLayout(layout)

    
    def _update_valid_start(self):
        if self.get_file_path() and self.get_title() and self.get_tags() and self.get_artist() and self.get_song():
            self.task_bar.set_valid_start(True)
        
        else:
            self.task_bar.set_valid_start(False)


    def get_file_path(self):
        return self.file_upload.get_path()


    def get_title(self):
        return self.title.text()


    def get_tags(self):
        return self.tags.text()
    

    def get_artist(self):
        return self.artist.text()


    def get_song(self):
        return self.song.text()
    

    def get_thumbnail_check(self):
        return self.thumbnail_check.isChecked()


    def get_job(self):
        return {
            "file_path": self.get_file_path(),
            "title": self.get_title(),
            "tags": self.get_tags(),
            "artist": self.get_artist(),
            "song": self.get_song(),
            "thumbnail": self.get_thumbnail_check()
        }