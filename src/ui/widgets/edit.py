from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QLineEdit, QSlider
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QIcon, QColor, QPalette
from superqt import QRangeSlider
from src.ui.components.file_upload import FileUpload
from src.ui.components.task_bar import TaskBar


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
				padding: 8px;
				font-size: 12px;
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
				padding: 6px 10px;
				font-weight: bold;
				font-size: 12px
			}

			QPushButton:hover {
				background-color: #5ba1f0;
			}

			QPushButton:pressed {
				background-color: #3a7fcf;
			}

			QLabel {
				font-size: 24px;
				color: #000000;
			}

			QCheckBox {
				color: #000000;
				font-size: 14px;
				spacing: 8px;
			}

			QRangeSlider::sub-page:horizontal {
				background: #d9caa3;
			}

			QRangeSlider::handle:horizontal {
				background: #ffffff;
				border: 2px solid #888;
				margin: -6px 0;
				border-radius: 2px;
			}

			QRangeSlider::handle:horizontal:hover {
				background: #f0f8ff;
				border: 2px solid #5aa9ff;
			}

			QRangeSlider::handle:horizontal:pressed {
				background: #d9ecff;
				border: 2px solid #1d6fd8;
			}
		"""

		self.setStyleSheet(layout_style)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignTop)
		layout.setContentsMargins(50, 50, 50, 0)
		layout.setSpacing(12)

		self.video_upload = FileUpload("Video", "Select a video to edit", set_read_only=True)
		self.output_path = FileUpload("Output", "Select a folder to output video", set_read_only=True)
		self.filename = QLineEdit()
		self.filename.setPlaceholderText("Output Filename")

		# Video Container
		video_layout = QHBoxLayout()
		video_layout.setAlignment(Qt.AlignCenter)

		self.video_widget = QVideoWidget()
		self.video_widget.setFixedSize(896, 504)

		self.media_player = QMediaPlayer()
		self.audio = QAudioOutput()

		self.media_player.setAudioOutput(self.audio)
		self.media_player.setVideoOutput(self.video_widget)

		video_layout.addWidget(self.video_widget)

		# Video Controls
		control_layout = QHBoxLayout()
		control_layout.setAlignment(Qt.AlignCenter)

		self.slider = QRangeSlider(Qt.Horizontal)
		self.slider.setTickPosition(QSlider.TicksAbove)
		self.slider.setRange(0, 3000)
		self.slider.setValue((0, 1500, 3000))
		self._last_values = self.slider.value()

		self.play_button = QPushButton("Play")
		self.play_button.setIcon(QIcon("data/assets/icons/play.png"))
		self.play_button.setIconSize(QSize(16, 16))
		self.pause_button = QPushButton("Pause")
		self.pause_button.setIcon(QIcon("data/assets/icons/pause.png"))
		self.pause_button.setIconSize(QSize(16, 16))

		control_layout.addWidget(self.play_button)
		control_layout.addWidget(self.pause_button)

		# Edit Controls
		edit_layout = QHBoxLayout()
		edit_layout.setAlignment(Qt.AlignLeft)

		self.crop_check = QCheckBox()
		self.crop_check.setText("Crop to selected range")

		# Taskbar
		self.task_bar = TaskBar()
		self.task_bar.setContentsMargins(0, 0, 0, 0)

		# Layout Widgets
		layout.addWidget(self.video_upload)
		layout.addWidget(self.output_path)
		layout.addWidget(self.filename)
		layout.addLayout(video_layout)
		layout.addWidget(self.slider)
		layout.addLayout(control_layout)
		layout.addWidget(self.crop_check)
		layout.addWidget(self.task_bar)

		self.setLayout(layout)

		self.video_upload.path_changed.connect(self.load_video)
		self.media_player.durationChanged.connect(self._update_slider_range)

		self.play_button.clicked.connect(self.play)
		self.pause_button.clicked.connect(self.pause)

		self.slider.valueChanged.connect(self._on_value_changed)



	def load_video(self, path):
		self.media_player.setSource(QUrl.fromLocalFile(path))

		self.slider.setRange(0, self.media_player.duration())
		self.slider.setValue((0, 0, self.media_player.duration()))


	def play(self):
		self.media_player.play()


	def pause(self):
		self.media_player.pause()
		

	def _update_video_position(self, slider_idx):
		self.media_player.setPosition(self.slider.value()[slider_idx])

	def _on_value_changed(self, values):
		for i, (old, new) in enumerate(zip(self._last_values, values)):
			if old != new:
				self._update_video_position(i)

		self._last_values = values


	def _update_slider_range(self, duration):
		self.slider.setRange(0, duration)
		self.slider.setValue((0, int(duration/2), duration))
		

	def _update_valid_start(self):
		if self.valid_url and (self.get_video_check() or self.get_audio_check()):
			self.task_bar.set_valid_start(True)