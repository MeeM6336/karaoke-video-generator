import argparse
import subprocess


def crop_video(input_path, output_path, start_ms, end_ms):
    start = start_ms / 1000
    end = end_ms / 1000

    subprocess.run([
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-y",
        "-ss", str(start),
        "-to", str(end),
        "-i", input_path,
        "-c", "copy",
        output_path,
    ], check=True)


def merge_audio(video_path, new_audio_path, output_path):
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-y",
        "-i", video_path,
        "-i", new_audio_path,

        "-map", "0:v:0",
        "-map", "1:a:0",

        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "320k",

        "-shortest",

        output_path,
    ]

    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Crop videos",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--input_path",
        type=str,
        required=True,
        help="Input path to file"
    )

    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="Output path to file"
    )

    parser.add_argument(
        "--crop",
        action="store_true",
        default=False,
        required=False,
        help="Crop video?"
    )

    parser.add_argument(
        "--start",
        type=int,
        required=False,
        help="Start time in ms"
    )

    parser.add_argument(
        "--end",
        type=int,
        required=False,
        help="End time in ms"
    )

    parser.add_argument(
        "--audio_path",
        type=str,
        required=False,
        help="Path to audio file to merge audio"
    )

    args = parser.parse_args()

    if args.crop:
        crop_video(args.input_path, args.output_path, args.start, args.end)

    if args.audio_path:
        merge_audio(args.input_path, args.audio_path, args.output_path)


if __name__ == "__main__":
    main()