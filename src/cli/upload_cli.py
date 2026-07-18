import argparse
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# python src/upload_video.py --title "Wallows - Uncomfortable (Karaoke)" --video_path "output/uncomfortable.mp4" --tags "karaoke,lyrics,music,wallows" --artist "Wallows" --song "Uncomfortable"

CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "data/oauth/token.json"


def authenticate_youtube():
  creds = None

  if Path(TOKEN_FILE).exists():
    creds = Credentials.from_authorized_user_file(
      TOKEN_FILE,
      SCOPES
    )

  if not creds or not creds.valid:

    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())

    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        SCOPES
      )

      creds = flow.run_local_server(port=0)

    Path(TOKEN_FILE).parent.mkdir(parents=True, exist_ok=True)

    with open(TOKEN_FILE, "w") as f:
      f.write(creds.to_json())

  return build("youtube", "v3", credentials=creds)


def upload_video_to_youtube(youtube, video_file, title, artist, song, tags=None):
  description = f"""
    #Karaoke #Lyrics #Music #Karaokeversion

    🎤 Want to request your favorite songs? Leave a comment below and just wait for your best karaoke night
    
    🎵 Make sure to like & subscribe and hit the bell icon so you don't miss out on the latest songs
    
    ⭐ Original Song Credit:
    Originally performed  by artist {artist}

    Artist: {artist}
    Song: {song}

    Disclaimer:
    This karaoke/instrumental version was created for entertainment purposes. All rights to the original composition, lyrics, and master recording belong to their respective copyright owners.
    """

  request_body = {
    "snippet": {
      "title": title,
      "description": description,
      "tags": tags or [],
      "categoryId": "10"
    },
    "status": {
      "privacyStatus": "public"
    }
  }

  media_file = MediaFileUpload(video_file, chunksize=-1, resumable=True)

  request = youtube.videos().insert(
    part="snippet,status",
    body=request_body,
    media_body=media_file
  )

  response = None

  while response is None:
    print("Uploading file...")
    status, response = request.next_chunk()
    if response is not None:
      if 'id' in response:
        print(f"Video id '{response['id']}' was successfully uploaded.")

def main():
  youtube = authenticate_youtube()

  parser = argparse.ArgumentParser(
    description="Upload karaoke video to YouTube",
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

  parser.add_argument(
    "--artist",
    type=str,
    required=True,
    help="Artist name."
  )

  parser.add_argument(
    "--song",
    type=str,
    required=True,
    help="Song name."
  )

  args = parser.parse_args()

  video_file = args.video_path
  title = args.title
  tags = [tag.strip() for tag in args.tags.split(",")]
  artist = args.artist
  song = args.song

  upload_video_to_youtube(youtube, video_file, title, artist, song, tags)

if __name__ == "__main__":
  main()