import requests
import yt_dlp
import subprocess
from pathlib import Path
from pipeline.util import lrc_to_segments, to_json
from pipeline.ass_generation import aligned_segments_to_ass


def run_menu():
  while True:
    print("Please search for the song to sync lyrics too, or (-1) to skip and use WhisperX transcription:")
    query = input("> ").strip().lower()

    if query == "-1":
      return None, None

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
        continue

      results = response.json()

      for i, result in enumerate(results[:5], 1):
        print(f"{i} - {result['artistName']} - {result['trackName']} ({result['albumName']})")

      print("Select an input below")
      choice = int(input("> ").strip().lower()) - 1

      segments = lrc_to_segments(results[choice]['syncedLyrics'])

      return segments, results[choice]['trackName']

    except requests.exceptions.RequestException as e:
      print(f"Error fetching data: {e}")
      continue

    
def download_yt(url, output_dir):
  output_dir = Path(output_dir)
  output_file = str(output_dir / "%(title)s.%(ext)s")

  ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": output_file,
    "postprocessors": [
      {
        "key": "FFmpegExtractAudio",
        "preferredcodec": "wav"
      }
    ]
  }

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    original_file = ydl.prepare_filename(info)

  return str(Path(original_file).with_suffix(".wav"))


def video_generation(yt_link=None, audio_path="", video_path="", output_path=None, temp_dir=None):
  segments_path = None
  track_name = None

  audio_path = (
    audio_path
    if audio_path is not None
    else download_yt(yt_link, temp_dir)
  )

  segments, track_name = run_menu()
  
  if segments is not None:
    segments_path = to_json("segments", temp_dir, segments)

  result = subprocess.run(
    [
      r"demucs_venv\Scripts\python.exe",
      "src/pipeline/run_demucs.py",
      audio_path,
      str(temp_dir)
    ],
    capture_output=True,
    text=True,
    check=True
  )

  vocal_path = result.stdout.strip()
  cmd = [
    r"whisper_venv\Scripts\python.exe",
		"src/pipeline/run_whisperx.py"
  ]

  if segments_path is not None:
    cmd.append(segments_path)

  cmd.extend([
    vocal_path,
    str(temp_dir)
  ])

  result = subprocess.run(
    cmd,
    check=True
  )

  # Generate .ass file
  aligned_dir = temp_dir / "aligned_segments.json"
  ass_dir = temp_dir / "lyrics.ass"
  aligned_segments_to_ass(aligned_dir, ass_dir, track_name)

  # Create video
  instrumental_path = temp_dir / "htdemucs_ft" / Path(audio_path).stem / "no_vocals.wav"

  if output_path is None:
    output_path = temp_dir / "output_video.mp4"

  cmd = [
    "ffmpeg",

    "-stream_loop", "-1",

    "-i", video_path,
    "-i", instrumental_path,

    "-vf", f"ass=output/temp/lyrics.ass,scale=1920:1080",

    "-map", "0:v:0",
    "-map", "1:a:0",

    "-r", "30",

    "-c:v", "h264_nvenc",
    "-cq", "19",
    "-preset", "p5",

    "-c:a", "aac",
    "-b:a", "320k",

    "-shortest",

    str(output_path)
  ]

  subprocess.run(cmd, check=True)

  print(f"Output video saved to: {output_path}")