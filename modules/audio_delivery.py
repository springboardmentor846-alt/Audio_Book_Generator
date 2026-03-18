import os
import shutil
from pathlib import Path

def read_audio_bytes(audio_path: str) -> bytes:
    with open(audio_path, "rb") as f:
        return f.read()


def cleanup_temp_segments(directory: str) -> None:
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)


def ensure_directory(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def list_previous_audiobooks(output_dir: str) -> list[dict]:
    if not os.path.exists(output_dir):
        return []

    entries = []
    for fname in sorted(os.listdir(output_dir), reverse=True):
        if fname.endswith(".mp3"):
            full_path = os.path.join(output_dir, fname)
            size_kb = os.path.getsize(full_path) / 1024
            entries.append({"name": fname, "path": full_path, "size_kb": round(size_kb, 1)})
    return entries
