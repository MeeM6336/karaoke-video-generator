from pathlib import Path
import sys
import subprocess


audio_path = Path(sys.argv[1]).resolve()
output_dir = Path(sys.argv[2]).resolve()

model = "htdemucs_ft"

cmd = [
  sys.executable,
  "-m",
  "demucs",
  "--two-stems=vocals",
  "--shifts=10",
  "-n", model,
  "-o", str(output_dir),
  str(audio_path)
]

subprocess.run(
  cmd,
  check=True,
  stdout=subprocess.DEVNULL
)

song_name = audio_path.stem

vocals_path = (
  output_dir /
  model /
  song_name /
  "vocals.wav"
)

if not vocals_path.exists():
  raise FileNotFoundError(vocals_path)

print(vocals_path.resolve())