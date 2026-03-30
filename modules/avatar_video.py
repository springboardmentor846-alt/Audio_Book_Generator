import subprocess
import os
import time

def generate_avatar_video(audio_file):

    sadtalker_path = "SadTalker"
    output_dir = os.path.join(sadtalker_path, "results")

    python_path = os.path.join(
        sadtalker_path,
        "..",
        "sadtalker_env",
        "Scripts",
        "python.exe"
    )

    command = [
        python_path,
        "inference.py",
        "--driven_audio", f"../{audio_file}",
        "--source_image", "../avatar.jpg",
        "--result_dir", "results"
    ]

    subprocess.run(command, cwd=sadtalker_path)

    time.sleep(2)

    files = os.listdir(output_dir)
    files = sorted(files, key=lambda x: os.path.getctime(os.path.join(output_dir, x)))

    latest_video = os.path.join(output_dir, files[-1])

    return latest_video