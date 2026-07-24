import sys
import re
import requests

from PySide6.QtCore import QProcess
from pathlib import Path
from src.ui.components.missing_dialog import MissingDialog
from src.ui.components.lyrics_dialog import LyricsDialog
from src.ui.components.job_completion_dialog import JobCompletionDialog


class MainController:

    def __init__(self, window):
        self.window = window
        self.current_page = 0
        self.job_type = None

        self.process = QProcess()

        self.window.create_widget.search_request.connect(
            self.search_lyrics
        )
        self.process.readyReadStandardOutput.connect(self.read_stdout)
        self.process.readyReadStandardError.connect(self.read_stderr)
        self.process.finished.connect(self.process_finished)


    def missing_dialog(self, missing):
        dialog = MissingDialog(missing)

        dialog.exec()


    def job_completion_dialog(self, job_name):
        dialog = JobCompletionDialog(job_name)

        dialog.exec()


    def search_lyrics(self, query):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:
            url = "https://lrclib.net/api/search"
            params = {
                "q": query
            }
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()

            if response.status_code == 204:
                print("No results found. Please try a different search.")
                return

            results = response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return

        dialog = LyricsDialog(results)

        if dialog.exec():
            result = dialog.selected_result()
            self.window.create_widget.set_lyrics(result["syncedLyrics"])
        else:
            return


    def validate_url(self, text):
        valid_urls = (
            "https://youtu.be/",
            "https://www.youtube.com/",
            "www.youtube.com/",
            "www.youtu.be/",
            "youtu.be/",
            "youtube.com/"
        )

        return text.startswith(valid_urls)


    def start_create_job(self):
        self.job_type = "create"

        job = self.window.create_widget.get_job()
        missing = []

        # Input validation
        if not job["yt_link"] and (not job["audio_file"] or not job["video_file"]):
            missing.append("YouTube link or both audio file and video file")

        if job["yt_link"] and not self.validate_url(job["yt_link"]):
            missing.append("Valid YouTube link")

        if missing:
            self.missing_dialog(missing)
            return

        cmd = ["-m", "src.cli.create_cli"]

        if job["yt_link"]:
            cmd.extend(["--yt_link", job["yt_link"]])

        if job["audio_file"]:
            cmd.extend(["--audio_file", job["audio_file"]])

        if job["video_file"]:
            cmd.extend(["--video_file", job["video_file"]])

        if job["output_dir"] and job["filename"]:
            output_path = Path(job["output_dir"]) / f"{job['filename']}.mp4"
            cmd.extend(["--output_file", str(output_path)])

        if job["font_color"]:
            cmd.extend(["--font_color", job["font_color"]])

        if job["lyrics"]:
            cmd.extend(["--lyrics", job["lyrics"]])
        else:
            cmd.extend(["--lyrics", "-1"])

        self.process.start(sys.executable, cmd)


    def start_convert_job(self):
        self.job_type = "convert"

        job = self.window.convert_widget.get_job()
        missing = []

        if not job["yt_link"]:
            missing.append("YouTube link")
        elif not self.validate_url(job["yt_link"]):
            missing.append("Valid YouTube link")

        if not job["audio"] and not job["video"]:
            missing.append("Audio and/or Video")

        if missing:
            self.missing_dialog(missing)
            return

        output_dir = job["output_dir"] or "output"
        filename = job["filename"] or "output_vid"

        cmd = [
            "-m",
            "src.cli.convert_cli",
            "--yt_link",
            job["yt_link"],
            "--output_dir",
            output_dir,
            "--filename", 
            filename
        ]

        if job["audio"]:
            cmd.append("--audio")

        if job["video"]:
            cmd.append("--video")

        self.process.start(sys.executable, cmd)

    
    def start_upload_job(self):
        self.job_type = "upload"

        job = self.window.upload_widget.get_job()
        missing = []

        if not job["file_path"]:
            missing.append("Video")

        if not job["title"]:
            missing.append("Title")

        if not job["tags"]:
            missing.append("Tags")

        if not job["artist"]:
            missing.append("Artist")

        if not job["song"]:
            missing.append("Song")

        if missing:
            self.missing_dialog(missing)
            return

        cmd = [
            "-m",
            "src.cli.upload_cli",
            "--video_path",
            job["file_path"],
            "--title",
            job["title"],
            "--tags",
            job["tags"],
            "--artist",
            job["artist"],
            "--song",
            job["song"],
        ]

        if job["thumbnail"]:
            cmd.extend(["--thumbnail"])

        self.process.start(sys.executable, cmd)


    def start_edit_job(self):
        self.job_type = "edit"

        job = self.window.edit_widget.get_job()
        missing = []

        if not job["input_path"]:
            missing.append("Input video")

        if job["crop"]:
            if job["start"] is None or job["end"] is None:
                missing.append("Crop start/end times")

        if missing:
            self.missing_dialog(missing)
            return

        output_dir = job["output_dir"] or "output"
        filename = job["filename"] or "edited_video"

        output_path = Path(output_dir) / f"{filename}.mp4"

        cmd = [
            "-m",
            "src.cli.edit_cli",
            "--input_path",
            job["input_path"],
            "--output_path",
            str(output_path),
        ]

        if job["crop"]:
            cmd.extend([
                "--crop",
                "--start",
                str(job["start"]),
                "--end",
                str(job["end"]),
            ])

        self.process.start(sys.executable, cmd)


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
        if exit_code == 0:
            self.set_progress(progress=100)
            self.job_completion_dialog(self.job_type, "completed successfully")

        else:
            self.job_completion_dialog(self.job_type, f"failed with error code {exit_code}")


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