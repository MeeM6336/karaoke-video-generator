import argparse

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# python src/upload_video.py --title "Wallows - At The End of the Day (Karaoke Version)" --video_path "output/at the end of the day.mp4" --tags "karaoke,lyrics,music,wallows"


CLIENT_SECRETS_FILE = "client_secrets.json"


def authenticate_youtube():
  SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

  flow = InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    SCOPES
  )

  credentials = flow.run_local_server(port=0)

  youtube = build("youtube", "v3", credentials=credentials)

  return youtube


def upload_video_to_youtube(youtube, video_file, title, tags=None):
  print(f"Uploading video: {video_file} with title: '{title}' and tags: {tags}")

  request_body = {
    "snippet": {
      "title": title,
      "description": f"Karaoke lyric video for {title}",
      "tags": tags or [],
      "categoryId": "10"
    },
    "status": {
      "privacyStatus": "private"
    }
  }

  media_file = MediaFileUpload(video_file, chunksize=-1, resumable=True)

  youtube.videos().insert(
    part="snippet,status",
    body=request_body,
    media_body=media_file
  )

  print(f"Upload complete!")


def main():
  youtube = authenticate_youtube()

  parser = argparse.ArgumentParser(
    description="Generate a karaoke video with synchronized lyrics.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )

  parser.add_argument(
    "--video_path",
    type=str,
    required=True,
    help="Path to the video file to upload."
  )

  parser.add_argument(
    "--title",
    type=str,
    required=True,
    help="Title for the video."
  )

  parser.add_argument(
    "--tags",
    type=str,
    required=True,
    help="Comma-separated tags for the video."
  )

  args = parser.parse_args()

  video_file = args.video_path
  title = args.title
  tags = [tag.strip() for tag in args.tags.split(",")]

  upload_video_to_youtube(youtube, video_file, title, tags)

if __name__ == "__main__":
  main()

