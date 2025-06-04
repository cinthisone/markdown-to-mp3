import sys, os, subprocess, re
from TTS.api import TTS
import tempfile
import getpass
import torch

# Use a fixed reference WAV and language for XTTS-v2
speaker_wav = os.path.join(os.path.dirname(__file__), "refvoice", "refvoice.wav")
language = "en"

# Read input file from argument
input_file = sys.argv[1]
filename = os.path.splitext(os.path.basename(input_file))[0]

# Save to output folder inside project
output_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(output_dir, exist_ok=True)

# Dynamically detect Windows username for Downloads path
windows_username = None
# Try to extract from input path if possible
if input_file.startswith("/mnt/c/Users/"):
    parts = input_file.split("/")
    if len(parts) > 4:
        windows_username = parts[4]
if not windows_username:
    # Fallback to WSL username if available
    try:
        import pwd
        windows_username = getpass.getuser()
    except Exception:
        windows_username = "info"  # fallback default
windows_downloads = f"/mnt/c/Users/{windows_username}/Downloads"
mp3_path = os.path.join(windows_downloads, f"{filename}.mp3")

# Read note and clean markdown
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# Remove code blocks (```...```), inline code (`...`), HTML tags, and markdown syntax
text = re.sub(r"```[\s\S]*?```", " ", text)  # Remove code blocks
text = re.sub(r"`[^`]*`", " ", text)           # Remove inline code
text = re.sub(r"<[^>]+>", " ", text)           # Remove HTML tags
text = re.sub(r"[#*_\-\[\]()>~]", " ", text) # Remove markdown special chars
text = re.sub(r"!\[[^\]]*\]\([^\)]*\)", " ", text) # Remove images
text = re.sub(r"\[[^\]]*\]\([^\)]*\)", " ", text)  # Remove links
text = re.sub(r"\s+", " ", text)              # Collapse whitespace
text = text.strip()

# Filter out very short lines to avoid TTS model errors
lines = [line.strip() for line in text.splitlines() if len(line.strip()) >= 10]
filtered_text = " ".join(lines)
filtered_text = filtered_text[:50000]  # Allow more text for chunking

# Split into 500–1000 char chunks
chunks = []
chunk = ""
for word in filtered_text.split():
    if len(chunk) + len(word) + 1 > 1000:
        if len(chunk) >= 500:
            chunks.append(chunk.strip())
            chunk = word
        else:
            chunk += " " + word
    else:
        chunk += (" " if chunk else "") + word
if 500 <= len(chunk) <= 1000:
    chunks.append(chunk.strip())
elif chunk:
    # If last chunk is short, append to previous if possible
    if chunks and len(chunks[-1]) + len(chunk) <= 1000:
        chunks[-1] += " " + chunk
    else:
        chunks.append(chunk.strip())

# Initialize TTS with VITS (best available in TTS 0.13.3)
tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=False)

# Generate wav for each chunk, then concatenate
wav_files = []
for i, chunk in enumerate(chunks):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{i}.wav") as tmp_wav:
            tts.tts_to_file(text=chunk, file_path=tmp_wav.name)
            wav_files.append(tmp_wav.name)
    except Exception as e:
        print(f"⚠️ Error processing chunk {i}: {e}")
        continue

if not wav_files:
    print("❌ No audio chunks were generated. Exiting.")
    sys.exit(1)

# Concatenate wav files using ffmpeg
concat_list_path = os.path.join(output_dir, f"{filename}_concat.txt")
with open(concat_list_path, "w") as f:
    for wav in wav_files:
        f.write(f"file '{wav}'\n")

wav_path = os.path.join(output_dir, f"{filename}_final.wav")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", wav_path])

# Convert to MP3
subprocess.run(["ffmpeg", "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-qscale:a", "4", mp3_path])

# Also copy MP3 to Windows Downloads folder if not already there
try:
    if mp3_path != os.path.join(output_dir, f"{filename}.mp3"):
        import shutil
        shutil.copy2(os.path.join(output_dir, f"{filename}.mp3"), mp3_path)
        print(f"✅ MP3 also copied to: {mp3_path}")
except Exception as e:
    print(f"⚠️ Could not copy MP3 to Windows Downloads folder: {e}")

# Cleanup temp files
for wav in wav_files:
    os.remove(wav)
os.remove(wav_path)
os.remove(concat_list_path)

print(f"✅ MP3 saved to: {os.path.join(output_dir, f'{filename}.mp3')}")
