import argparse
import subprocess


def crop_video(input_path, output_path, start_ms, end_ms):
    start = start_ms / 1000
    end = end_ms / 1000

    subprocess.run([
        "ffmpeg",
        "-y",
        "-ss", str(start),
        "-to", str(end),
        "-i", input_path,
        "-c", "copy",
        output_path,
    ], check=True)


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
        required=True,
        help="End time in ms"
    )

    args = parser.parse_args()

    crop_video(args.input_path, args.output_path, args.start, args.end)

if __name__ == "__main__":
    main()