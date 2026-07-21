import argparse
import shutil
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from PIL import Image, ImageDraw, ImageFont


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


def upload_video_to_youtube(youtube, video_file, title, artist, song, thumbnail_path=None, tags=None):
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

  media_file = MediaFileUpload(video_file, chunksize=(16 * 1024 * 1024), resumable=True)

  request = youtube.videos().insert(
    part="snippet,status",
    body=request_body,
    media_body=media_file
  )

  response = None

  while response is None:
    status, response = request.next_chunk()
    if status:
      progress = int(status.progress() * 100)
      print(f"[PROGRESS] - {progress}%", flush=True)
      
    if 'id' in response:
      print(f"Video id '{response['id']}' was successfully uploaded.")
  
  video_id = response["id"]

  if thumbnail_path:
    youtube.thumbnails().set(
      videoId=video_id,
      media_body=MediaFileUpload(
        thumbnail_path,
        mimetype="image/png"
      )
    ).execute()


def wrap_text(draw, text, font, max_width):
  words = text.split()
  lines = []
  current = ""

  for word in words:
    test = word if current == "" else current + " " + word

    bbox = draw.textbbox((0, 0), test, font=font)
    width = bbox[2] - bbox[0]

    if width <= max_width:
      current = test
    else:
      if current:
        lines.append(current)
      current = word

  if current:
    lines.append(current)

  return lines

def draw_centered(draw, text, font, y, image_width, font_color="white", max_width=None, line_spacing=0):
  if max_width is None:
    max_width = image_width

  lines = wrap_text(draw, text, font, max_width)

  ascent, descent = font.getmetrics()
  line_height = ascent + descent + line_spacing

  for i, line in enumerate(lines):
    bbox = draw.textbbox((0, 0), line, font=font)
    width = bbox[2] - bbox[0]

    x = (image_width - width) // 2

    draw.text(
      (x, y + i * line_height),
      line,
      font=font,
      fill=font_color,
      stroke_width=8,
      stroke_fill="black"
    )


def create_thumbnail(song, artist):
  output_dir = Path("output/temp/thumbnail")
  output_dir.mkdir(parents=True, exist_ok=True)

  img = Image.open("data/assets/thumbnail.png")
  draw = ImageDraw.Draw(img)

  font_song = ImageFont.truetype(
    "data/assets/fonts/Sweet Cucumber Mocktail.ttf", 200
  )

  font_artist = ImageFont.truetype(
    "data/assets/fonts/Sweet Cucumber Mocktail.ttf", 190
  )

  font_subtitle = ImageFont.truetype(
    "data/assets/fonts/Sweet Cucumber Mocktail.ttf", 75
  )

  draw_centered(draw, song, font_song, 50, img.width, font_color="#7abaff")
  draw_centered(draw, artist, font_artist, 450, img.width)
  draw_centered(draw, "Karaoke Version", font_subtitle, 670, img.width, font_color="#8a8a8a")

  img.save(output_dir / f"{song} - {artist} thumbnail.png", quality=100)

  return str(output_dir / f"{song} - {artist} thumbnail.png")


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

  parser.add_argument(
    "--thumbnail",
    action="store_true",
    default=False,
    help="Auto generate thumbnail"
  )

  args = parser.parse_args()

  video_file = args.video_path
  title = args.title
  tags = [tag.strip() for tag in args.tags.split(",")]
  artist = args.artist
  song = args.song
  thumbnail_path = None

  if args.thumbnail:
   thumbnail_path =  create_thumbnail(song, artist)

  upload_video_to_youtube(youtube, video_file, title, artist, song, thumbnail_path, tags)

  if args.thumbnail:
    shutil.rmtree(thumbnail_path, ignore_errors=True)


if __name__ == "__main__":
  main()