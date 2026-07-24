from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QListWidget, QListWidgetItem, QPlainTextEdit
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt


class LyricsDialog(QDialog):
    def __init__(self, query_results):
        super().__init__()

        self.setWindowTitle("Lyric Selection")
        self.setWindowIcon(QIcon("data/assets/icons/logo.png"))
        
        self.resize(800, 600)
        
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

        self.instructions = QLabel()
        self.instructions.setText("Select the song according to your search")
        self.preview_label = QLabel()
        self.preview_label.setText("Preview of lyrics:")

        self.list = QListWidget()
        for result in query_results[:10]:
            if result.get("syncedLyrics"):

                minutes, seconds = divmod(int(result["duration"]), 60) if result.get("duration") else (0, 0)

                item = QListWidgetItem(
                    f"{result["artistName"]} - {result["trackName"]} - ({minutes}:{seconds:02})"
                )

                item.setData(
                    Qt.UserRole,
                    result
                )

                self.list.addItem(item)
        self.list.currentItemChanged.connect(self._on_selection_changed)

        ok_btn = QDialogButtonBox.Ok
        cancel_btn = QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(ok_btn | cancel_btn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.instructions)
        layout.addWidget(self.list)
        layout.addWidget(self.preview_label)
        layout.addWidget(self.preview)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def selected_result(self):
        item = self.list.currentItem()

        if item is None:
            return None

        return item.data(Qt.UserRole)

    def _on_selection_changed(self, curr, prev):
        if curr is None:
            return
        
        result = curr.data(Qt.UserRole) 
        self.preview.setPlainText(result["syncedLyrics"])