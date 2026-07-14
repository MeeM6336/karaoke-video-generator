from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout, QFileDialog
from PySide6.QtCore import Qt, Signal

class FileUpload(QWidget):
    path_changed = Signal(str)
    
    def __init__(self, file_type, placeholder_text="Select a file", set_read_only=True):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        self.file_type = file_type
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText(placeholder_text)
        if set_read_only:
            self.file_path.setReadOnly(True)

        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.select_file)

        layout.addWidget(self.file_path)
        layout.addWidget(browse_btn)

        self.setLayout(layout)

    def select_file(self):
        if self.file_type.lower() == "output":
            filename = QFileDialog.getExistingDirectory(
                self,
                f"Choose {self.file_type} Directory",
                ""
            )

        else:
            filename, _ = QFileDialog.getOpenFileName(
                self,
                f"Choose {self.file_type} File",
                "",
                f"All Files (*)"
            )

        if filename:
            self.file_path.setText(filename)

            try:
                self.path_changed.emit(filename)
            except Exception:
                pass

    def get_path(self):
        return self.file_path.text()