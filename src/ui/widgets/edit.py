from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QIcon
from src.ui.components.file_upload import FileUpload


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
		layout.setAlignment(Qt.AlignTop)
		layout.setContentsMargins(50, 50, 50, 0)
		layout.setSpacing(20)

		control_layout = QHBoxLayout()
		control_layout.setAlignment(Qt.AlignCenter)

		self.video_upload = FileUpload("Video", "Select a video to edit", set_read_only=True)

		self.video_widget = QVideoWidget()
		self.video_widget.setFixedSize(1024, 576)
		self.video_widget.setStyleSheet("background-color: #ffffff;")

		self.media_player = QMediaPlayer()
		self.audio = QAudioOutput()

		self.media_player.setAudioOutput(self.audio)
		self.media_player.setVideoOutput(self.video_widget)

		# Video Controls
		self.play_button = QPushButton("Play")
		self.play_button.setIcon(QIcon("data/assets/icons/play.png"))
		self.play_button.setIconSize(QSize(24, 24))
		self.pause_button = QPushButton("Pause")
		self.pause_button.setIcon(QIcon("data/assets/icons/pause.png"))
		self.pause_button.setIconSize(QSize(24, 24))

		layout.addWidget(self.video_upload)
		layout.addWidget(self.video_widget)
		control_layout.addWidget(self.play_button)
		control_layout.addWidget(self.pause_button)
		layout.addLayout(control_layout)

		self.setLayout(layout)

		self.video_upload.path_changed.connect(self.load_video)
		self.play_button.clicked.connect(self.play)
		self.pause_button.clicked.connect(self.pause)

	def load_video(self, path):
		self.media_player.setSource(QUrl.fromLocalFile(path))
		self.media_player.play()

	def play(self):
		self.media_player.play()

	def pause(self):
		self.media_player.pause()
		
