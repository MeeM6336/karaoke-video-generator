import re
import json
from pathlib import Path
import sys
import os

def to_json(filename, output_dir, segments):
  json_path = os.path.join(output_dir, f"{filename}.json")

  with open(json_path, "w", encoding="utf-8") as f:
    json.dump(segments, f, indent=4)
  
  return json_path


def lrc_to_segments(lrc_text, lyric_type):
  if lyric_type == "synced":
    pattern = re.compile(r"\[(\d+):(\d+\.\d+)\]\s*(.*)")

    entries = []

    for line in lrc_text.splitlines():
      match = pattern.match(line)
      if not match:
        continue

      minutes = int(match.group(1))
      seconds = float(match.group(2))
      text = match.group(3).strip()

      if not text:
        continue

      start = minutes * 60 + seconds

      entries.append({
        "text": text,
        "start": start
      })

    entries.sort(key=lambda x: x["start"])

    segments = []
    for i in range(len(entries)):
      start = entries[i]["start"]
      end = entries[i + 1]["start"] if i + 1 < len(entries) else start + 4.0

      segment_text = entries[i]["text"]
      cleaned_segment_text = re.sub(r"\s*\([^)]*\)", "", segment_text)

      segments.append({
        "text": cleaned_segment_text,
        "start": start,
        "end": end
      })

    return segments

  elif lyric_type == "plain":
    segments = []

    for line in lrc_text.splitlines():
      line = line.strip()

      if not line:
        continue

      segments.append({
        "start": 0.0,
        "end": 0.0,
        "text": line,
      })

    return segments