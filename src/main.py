from pathlib import Path
import subprocess
import argparse
import requests
import yt_dlp
from util import lrc_to_segments, to_json
import os
import shutil
import sys
from ass_generation import aligned_segments_to_ass


# python src/main.py  --audio_file "data/ayby.mp3" --video_file "data/beach2.mp4" --output_file "data/ayby_karaoke.mp4"
# python src/main.py  --yt_link "https://www.youtube.com/watch?v=x7mHRNfo-zc" --video_file "data/beach2.mp4" --output_file "output/at the end of the day.mp4"
# python src/main.py  --yt_link "https://www.youtube.com/watch?v=Y6yLKQV4lrM" --video_file "data/beach2.mp4" --output_file "output/id.mp4"
# python src/main.py  --audio_file "data/keshi - Touch.mp3" --video_file "data/beach2.mp4" --output_file "output/keshi - Touch.mp4"
# python src/main.py  --yt_link "https://www.youtube.com/watch?v=33kwtdW-6xY" --video_file "data/beach2.mp4" --output_file "output/alright.mp4"

def run_menu():
  while True:
    print("Please search for the song to sync lyrics too, or (-1) to skip:")
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


def main():
  current_dir = Path(__file__).resolve().parent
  project_root = current_dir.parent
  output_dir = project_root / "output"
  output_dir.mkdir(exist_ok=True)
  temp_dir = project_root / "output" / "temp"
  temp_dir.mkdir(exist_ok=True)
  sys.path.append(os.path.join(current_dir, '..'))

  segments_path = None
  track_name = None

  parser = argparse.ArgumentParser(
    description="Generate a karaoke video with synchronized lyrics.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )

  parser.add_argument(
    "--yt_link",
    type=str,
    required=False,
    help="YouTube link for the song."
  )

  parser.add_argument(
    "--audio_file",
    type=str,
    required=False,
    help="Path to the input audio file (.mp3, .wav)."
  )

  parser.add_argument(
    "--video_file",
    type=str,
    required=True,
    help="Path to the input background video file (.mp4)."
  )

  parser.add_argument(
    "--output_file",
    type=str,
    required=False,
    help="Path to the output video file (.mp4)."
  )

  # Argument parsing and validation
  args = parser.parse_args()
  if args.audio_file is None and args.yt_link is None:
    print("Either --audio_file or --yt_link must be provided.")
    sys.exit(1)

  if not os.path.exists(args.video_file):
    print(f"Video file not found: {args.video_file}")
    sys.exit(1)

  audio_path = (
    args.audio_file
    if args.audio_file is not None
    else download_yt(args.yt_link, temp_dir)
  )

  print(f"Audio file path: {audio_path}") # Debug

  if not os.path.exists(audio_path):
    print(f"Audio file not found: {audio_path}")
    sys.exit(1)

  segments, track_name = run_menu()
  
  if segments is not None:
    segments_path = to_json("segments", temp_dir, segments)

  result = subprocess.run(
    [
      r"demucs_venv\Scripts\python.exe",
      "src/run_demucs.py",
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
		"src/run_whisperx.py"
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
  output_file = args.output_file
  if args.output_file is None:
    output_file = temp_dir / "output_video.mp4"

  cmd = [
    "ffmpeg",

    "-stream_loop", "-1",

    "-i", args.video_file,
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

    str(output_file)
]

  subprocess.run(cmd, check=True)

  print(f"Output video saved to: {output_file}")

  # Cleanup
  shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
  main()