import requests
import yt_dlp
import subprocess
from pathlib import Path
from src.util.util import lrc_to_segments, to_json
from src.karaoke_pipeline.ass_generation import aligned_segments_to_ass

def get_lyrics(query):
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

    return results

  except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    return


def run_menu():
  while True:
    print("Please search for the song to sync lyrics too, or (-1) to skip and use WhisperX transcription:")
    query = input("> ").strip().lower()

    if query == "-1":
      return None, None

    results = get_lyrics(query)

    for i, result in enumerate(results[:5], 1):
      print(f"{i} - {result['artistName']} - {result['trackName']} ({result['albumName']})")

    print("Select an input below")
    choice = int(input("> ").strip().lower()) - 1

    segments = lrc_to_segments(results[choice]['syncedLyrics'])

    return segments

    
def download_yt(download_type, url, output_dir):
  output_dir = Path(output_dir)
  output_template = str(output_dir / "%(title)s.%(ext)s")

  ydl_opts = {
    "outtmpl": output_template,
    "cookiesfrombrowser": ("firefox",),
    "js_runtimes": {
        "node": {}
    },
    "remote_components": ["ejs:github"]
  }

  if download_type == "audio":
    ydl_opts["format"] = "bestaudio"
    ydl_opts["postprocessors"] = [{
      "key": "FFmpegExtractAudio",
      "preferredcodec": "wav",
    }]

  elif download_type == "video":
    ydl_opts["format"] = "bestvideo[ext=mp4]/bestvideo"

  else:
    raise ValueError("download_type must be 'audio' or 'video'")

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    original_file = Path(ydl.prepare_filename(info))

  if download_type == "audio":
    return str(original_file.with_suffix(".wav"))
  else:
    return str(original_file.with_suffix(".mp4"))


def video_generation(font_color, yt_link=None, audio_path="", video_path="", output_path=None, temp_dir=None, lyrics=None):
  segments_path = None

  audio_path = (
    audio_path
    if audio_path is not None
    else download_yt("audio", yt_link, temp_dir)
  )

  video_path = (
    video_path
    if video_path is not None
    else download_yt("video", yt_link, temp_dir)
  )

  if output_path is None:
    output_path = "output/output_video.mp4"

  if lyrics is None:
    segments = run_menu()

  else:
    segments = lrc_to_segments(lyrics)
  
  if segments is not None:
    segments_path = to_json("segments", temp_dir, segments)

  print("[PROGRESS] - 10%", flush=True)

  result = subprocess.run(
    [
      r"demucs_venv\Scripts\python.exe",
      "-m",
      "src.karaoke_pipeline.run_demucs",
      audio_path,
      str(temp_dir)
    ],
    capture_output=True,
    text=True,
    check=True
  )

  vocal_path = result.stdout.strip()

  print("[PROGRESS] - 50%", flush=True)

  cmd = [
    r"whisper_venv\Scripts\python.exe",
    "-m"
		"src.karaoke_pipeline.run_whisperx"
  ]

  if segments_path is not None:
    cmd.append(segments_path)

  cmd.extend([
    vocal_path,
    str(temp_dir)
  ])

  result = subprocess.run(
    cmd,
    check=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
  )

  print("[PROGRESS] - 60%", flush=True)

  # Generate .ass file
  aligned_dir = temp_dir / "aligned_segments.json"
  ass_dir = temp_dir / "lyrics.ass"
  aligned_segments_to_ass(aligned_dir, ass_dir, font_color)

  # Instrumental clean-up
  raw_instrumental_dir = temp_dir / "htdemucs_ft" / Path(audio_path).stem / "no_vocals.wav"
  model_path = Path(output_path).parent.parent / "data" / "model"
  final_instrumental_path = temp_dir / "audio-separator" / "no_vocals_(Instrumental)_UVR-MDX-NET-Inst_HQ_4.wav"

  cmd = [
    r"demucs_venv\Scripts\audio-separator.exe",
    str(raw_instrumental_dir),
    "--model_filename", "UVR-MDX-NET-Inst_HQ_4.onnx",
    "--model_file_dir", str(model_path),
    "--output_dir", str(temp_dir / "audio-separator"),
    "--output_format", "WAV"
]

  result = subprocess.run(
    cmd,
    check=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
  )

  print("[PROGRESS] - 80%", flush=True)

  filters = (
    "loudnorm"
  )

  # Create video
  cmd = [
    "ffmpeg",

    "-loglevel", "error",

    "-hide_banner",

    "-y",

    "-stream_loop", "-1",

    "-i", video_path,
    "-i", final_instrumental_path,

    "-filter:a", filters, 

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