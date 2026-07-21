from PySide6.QtCore import QProcess
from pathlib import Path
import sys
import re

class MainController:

    def __init__(self, window):
        self.window = window
        self.current_page = 0
        self.job_type = None

        self.process = QProcess()

        self.process.readyReadStandardOutput.connect(self.read_stdout)
        self.process.readyReadStandardError.connect(self.read_stderr)
        self.process.finished.connect(self.process_finished)


    def start_karaoke_job(self):
        self.job_type = "create"
        job = self.window.create_widget.get_job()

        cmd = ["-m", "src.cli.karaoke_cli"]

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


    def start_convert_job(self):
        self.job_type = "convert"
        job = self.window.convert_widget.get_job()

        cmd = ["-m",  "src.cli.convert_cli","--yt_link", job["yt_link"], "--output_dir", job["output_dir"]]

        if job["audio"]:
            cmd.append("--audio")
        
        if job["video"]:
            cmd.append("--video")

        self.process.start(
            sys.executable,
            cmd
        )

    
    def start_upload_job(self):
        self.job_type = "upload"
        job = self.window.upload_widget.get_job()

        cmd = ["-m",  "src.cli.upload_cli", "--video_path", job["file_path"], "--title", job["title"], "--tags", job["tags"], "--artist", job["artist"], "--song", job["song"]]

        if job["thumbnail"]:
            cmd.append("--thumbnail")

        self.process.start(
            sys.executable,
            cmd
        )


    def start_edit_job(self):
        self.job_type = "edit"
        job = self.window.edit_widget.get_job()

        file_path = f"{job["output_dir"]}/{job["filename"]}.mp4"

        cmd = ["-m", "src.cli.edit_cli", "--input_path", job["input_path"], "--output_path", file_path, "--crop", "--start", str(job["start"]), "--end", str(job["end"])]

        self.process.start(
            sys.executable,
            cmd
        )


    def change_page(self, index):
        self.current_page = index
        self.window.stacked_layout.setCurrentIndex(self.current_page)
        
    
    def read_stdout(self):
        text = bytes(
            self.process.readAllStandardOutput()
        ).decode(errors="replace")

        if text:
            self.set_progress(text=text)


    def read_stderr(self):
        text = bytes(
            self.process.readAllStandardError()
        ).decode(errors="replace")

        if text:
            print("STDERR:")
            print(text)


    def process_finished(self, exit_code, exit_status):
        print(f"Finished with exit code {exit_code}")
        self.set_progress(progress=100)


    def set_progress(self, text=None, progress=None):
        if self.job_type == "create":
            if text is not None:
                match = re.search(r"\[PROGRESS\]\s*-\s*(\d+(?:\.\d+)?)%", text)

                if match:
                    self.window.create_widget.task_bar.set_progress(int(float(match.group(1))))
            
            if progress == 100:
                self.window.create_widget.task_bar.set_progress(100)

        if self.job_type == "upload":
            if text is not None:
                match = re.search(r"\[PROGRESS\]\s*-\s*(\d+(?:\.\d+)?)%", text)

                if match:
                    self.window.upload_widget.task_bar.set_progress(int(float(match.group(1))))

        if self.job_type == "convert":
            if text is not None:
                match = re.search(r'(\d+(?:\.\d+)?)%', text)

                if match:
                    self.window.convert_widget.task_bar.set_progress(int(float(match.group(1))))

        if self.job_type == "edit":
            if progress == 100:
                self.window.edit_widget.task_bar.set_progress(100)