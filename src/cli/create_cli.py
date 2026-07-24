from pathlib import Path
import argparse
import os
import shutil
import sys
from src.karaoke_pipeline.video_generation import video_generation


def main():
  project_root = Path(__file__).resolve().parent.parent.parent
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

  parser.add_argument(
    "--lyrics",
    type=str,
    required=False,
    help="Synced lyrics"
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
    font_color=args.font_color,
    lyrics=args.query
  )

  # Cleanup
  shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
  main()