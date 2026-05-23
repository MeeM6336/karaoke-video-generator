import json
import sys
import whisperx
from util import to_json

with open(sys.argv[1]) as f:
  segments = json.load(f)

vocal_path = sys.argv[2]

device = "cuda"
batch_size = 16
compute_type = "float16"

model = whisperx.load_model("large-v3", device, compute_type=compute_type)
audio = whisperx.load_audio(vocal_path)

model, metadata = whisperx.load_align_model(language_code="en", device=device)
result = whisperx.align(segments, model, metadata, audio, device, return_char_alignments=False)

to_json("aligned_segments", result)

