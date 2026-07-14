from PySide6.QtCore import QThread, QProcess
from pathlib import Path
import sys

class MainController:

    def __init__(self, window):
        self.window = window
        self.current_page = 0
        self.process = QProcess()

        self.process.readyReadStandardOutput.connect(
            self.read_output
        )

        self.process.finished.connect(
            self.process_finished
        )


    def start_karaoke_job(self):
        cli_path = str(Path(__file__).parent.parent / "karaoke_cli.py")

        job = self.window.create_widget.get_job()

        cmd = [cli_path]

        if job["yt_link"]:
            cmd.extend(["--yt_link", job["yt_link"]])

        if job["audio_file"]:
            cmd.extend(["--audio_file", job["audio_file"]])

        if job["video_file"]:
            cmd.extend(["--video_file", job["video_file"]])

        if job["output_dir"] and job["filename"]:
            file_path = f"{job["output_dir"]}/{job["filename"]}.mp4"

            cmd.extend(["--output_file", file_path])

        if job["font_color"]:
            cmd.extend(["--font_color", job["font_color"]])

        if job["query"]:
            cmd.extend(["--query", job["query"]])
        
        self.process.start(
            sys.executable,
            cmd
        )

        #self.window.create_widget.taskbar.set_progress(10)
    
    
    def read_output(self):
        text = bytes(
            self.process.readAllStandardOutput()
        ).decode()

        print(text)


    def change_page(self, index):
        self.current_page = index
        self.window.stacked_layout.setCurrentIndex(self.current_page)
    
    def process_finished(self, exit_code, exit_status):
        print(f"Finished with exit code {exit_code}")