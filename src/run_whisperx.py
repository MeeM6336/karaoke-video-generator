import json
import sys
from pathlib import Path
import whisperx
from util import to_json


if len(sys.argv) == 4:
  segments_path = sys.argv[1]
  vocal_path = sys.argv[2]
  output_dir = Path(sys.argv[3]).resolve()
  use_segments = True

elif len(sys.argv) == 3:
  segments_path = None
  vocal_path = sys.argv[1]
  output_dir = Path(sys.argv[2]).resolve()

  use_segments = False

if use_segments:
  with open(segments_path) as f:
    try:
      segments = json.load(f)
    except Exception as e:
      print(f"Error loading segments: {e}\n")
      print("Using WhisperX alignment instead")
      use_segments = False

device = "cuda"
batch_size = 16
compute_type = "float16"

# Load audio
audio = whisperx.load_audio(vocal_path)

# Transcribe using WhisperX if no segments
if use_segments is False:
  model = whisperx.load_model("large-v3", device, compute_type=compute_type)

  result = model.transcribe(audio, batch_size=batch_size)
  segments = result["segments"]
  to_json("segments", output_dir, segments)

  model_a, metadata = whisperx.load_align_model(language_code="en", device=device)
  result = whisperx.align(segments, model_a, metadata, audio, device, return_char_alignments=False)

  new_segments = []

  for seg in result["segments"]:
    words = seg["words"]

    current_words = []

    for i, w in enumerate(words):
      current_words.append(w)

      word_text = w["word"].strip()

      # split if NEXT word starts uppercase
      should_split = False

      if i < len(words) - 1:
        next_word = words[i + 1]["word"].strip()

        if (
          len(next_word) > 0 and
          next_word[0].isupper()
        ):
          should_split = True

      if i == len(words) - 1:
        should_split = True

      if should_split:
        new_segments.append({
          "start": current_words[0]["start"],
          "end": current_words[-1]["end"],
          "text": " ".join(w["word"] for w in current_words),
          "words": current_words
        })

        current_words = []
  
    result["segments"] = new_segments

# Align if segments are given
else:
  model_a, metadata = whisperx.load_align_model(language_code="en", device=device)
  result = whisperx.align(segments, model_a, metadata, audio, device, return_char_alignments=False)

to_json("aligned_segments", output_dir, result)

