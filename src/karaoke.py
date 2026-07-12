from pathlib import Path
import argparse
import os
import shutil
import sys
from video.video_generation import video_generation

# python src/karaoke.py  --audio_file "data/ayby.mp3" --video_file "data/beach2.mp4" --output_file "data/ayby_karaoke.mp4"
# python src/karaoke.py  --yt_link "https://www.youtube.com/watch?v=x7mHRNfo-zc" --video_file "data/beach2.mp4" --output_file "output/at the end of the day.mp4"
# python src/karaoke.py  --yt_link "https://www.youtube.com/watch?v=Y6yLKQV4lrM" --video_file "data/beach2.mp4" --output_file "output/id.mp4"
# python src/karaoke.py  --audio_file "data/keshi - Touch.mp3" --video_file "data/beach2.mp4" --output_file "output/keshi - Touch.mp4"
# python src/karaoke.py  --yt_link "https://www.youtube.com/watch?v=33kwtdW-6xY" --output_file "output/alright.mp4" --font_color "#87CEEB"
# python src/karaoke.py  --yt_link "https://www.youtube.com/watch?v=ghUTY5zK-gQ" --output_file "output/WANTCHU.mp4"
# python src/karaoke.py  --audio_file "data/the one that got away.wav" --video_file "data/totga.mp4" --output_file "output/the one that got away.mp4" --font_color "#FF69B4"
# python src/karaoke.py  --yt_link "https://www.youtube.com/watch?v=5pG2VPXPITg" --video_file "data/2.mp4" --output_file "output/uncomfortable.mp4" --font_color "#6B93FF"
# python src/karaoke.py  --yt_link "https://www.youtube.com/watch?v=cfcNFoaplTw" --video_file "data/car_drive_night.mp4" --output_file "output/past won't leave my bed.mp4" --font_color "#ebd059"

def main():
  current_dir = Path(__file__).resolve().parent
  project_root = current_dir.parent
  output_dir = project_root / "output"
  output_dir.mkdir(exist_ok=True)
  temp_dir = project_root / "output" / "temp"
  temp_dir.mkdir(exist_ok=True)

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
    required=False,
    help="Path to the input background video file (.mp4)."
  )

  parser.add_argument(
    "--output_file",
    type=str,
    required=False,
    help="Path to the output video file (.mp4)."
  )

  parser.add_argument(
    "--font_color",
    type=str,
    required=False,
    default="#00FFFF",
    help="Font color for the karaoke text."
  )

  # Argument parsing and validation
  args = parser.parse_args()
  if args.audio_file is None and args.yt_link is None:
    print("Either --audio_file or --yt_link must be provided.")
    sys.exit(1)

  if args.video_file is None and args.yt_link is None:
    print("Either --video_file or --yt_link must be provided.")
    sys.exit(1)

  if args.audio_file is not None:
    if not os.path.exists(args.audio_file):
      print(f"Audio file not found: {args.audio_file}")
      sys.exit(1)

  if args.video_file is not None:
    if not os.path.exists(args.video_file):
      print(f"Video file not found: {args.video_file}")
      sys.exit(1)

  if args.font_color is not None and not args.font_color.startswith("#") and len(args.font_color) == 6:
    print(f"Invalid font color: {args.font_color}. Please provide a valid hex code (e.g., #00FFFF).")
    sys.exit(1)

  video_generation(
    yt_link=args.yt_link,
    audio_path=args.audio_file,
    video_path=args.video_file,
    output_path=args.output_file,
    temp_dir=temp_dir,
    font_color=args.font_color
  )

  # Cleanup
  shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
  main()