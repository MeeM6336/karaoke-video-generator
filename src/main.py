import subprocess
import argparse
import requests
from util import lrc_to_segments, to_json
import os
import sys


# python src/main.py  --audio_file "data/ayby.mp3" --video_file "data/beach2.mp4"


def run_menu():
  while True:
    print("Please search for the song to sync lyrics too:")
    query = input("> ").strip().lower()

    headers = {
      "User-Agent": "Mozilla/5.0"
    }

    try:
      url = "https://lrclib.net/api/search"
      params = {
        "track_name": query
      }
      response = requests.get(url, params=params, headers=headers)
      response.raise_for_status()
      results = response.json()
      for i, result in enumerate(results[:5], 1):
        print(f"{i} - {result['artistName']} - {result['trackName']} ({result['albumName']})")

        print("Select an input below")
        choice = int(input("> ").strip().lower()) - 1

        segments = lrc_to_segments(results[choice]['syncedLyrics'])

        return segments

    except requests.exceptions.RequestException as e:
      print(f"Error fetching data: {e}")
      continue


def main():
  current_dir = os.path.dirname(os.path.abspath(__file__))
  sys.path.append(os.path.join(current_dir, '..'))

  parser = argparse.ArgumentParser(
    description="Generate a karaoke video with synchronized lyrics.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )

  parser.add_argument(
    "--audio_file",
    type=str,
    required=True,
    help="Path to the input audio file (.mp3, .wav)."
  )

  parser.add_argument(
    "--video_file",
    type=str,
    required=True,
    help="Path to the input background video file (.mp4)."
  )

  args = parser.parse_args()
  if not os.path.exists(args.audio_file):
    print(f"Audio file not found: {args.audio_file}")
    sys.exit(1)
  if not os.path.exists(args.video_file):
    print(f"Video file not found: {args.video_file}")
    sys.exit(1)

  segments = run_menu()
  segments_path = to_json("segments", segments)

  result = subprocess.run(
    [
      r"demucs_venv\Scripts\python.exe",
      "src/run_demucs.py",
      args.audio_file
    ],
    capture_output=True,
    text=True,
    check=True
  )

  vocal_path = result.stdout.strip()

  subprocess.run([
		r"whisper_venv\Scripts\python.exe",
		"src/run_whisperx.py",
    segments_path,
    vocal_path
	])

if __name__ == "__main__":
  main()