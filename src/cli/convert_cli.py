from pathlib import Path
import argparse
import yt_dlp


def convert_yt(download_type, url, output_dir):
    output_dir = Path(output_dir)
    output_template = str(output_dir / "%(title)s.%(ext)s")

    ydl_opts = {
        "outtmpl": output_template,
        "js_runtimes": {
            "node": {}
        },

        "remote_components": ["ejs:github"],
    }

    if download_type == "audio":
        ydl_opts["format"] = "bestaudio"
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }]

    elif download_type == "video":
        ydl_opts["format"] = "bestvideo[ext=mp4]/bestvideo"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main():
    parser = argparse.ArgumentParser(
        description="YouTube to mp3/mp4",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--yt_link",
        type=str,
        required=True,
        help="YouTube link"
    )

    parser.add_argument(
        "--audio",
        action="store_true",
        default=False,
        required=False,
        help="To audio?"
    )

    parser.add_argument(
        "--video",
        action="store_true",
        default=False,
        required=False,
        help="To video?"
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="Output file path"
    )

    args = parser.parse_args()

    if args.audio:
        print("Converting to audio...")
        convert_yt("audio", args.yt_link, args.output_dir)

    elif args.video:
        print("Converting to video...")
        convert_yt("video", args.yt_link, args.output_dir)

if __name__ == "__main__":
    main()

