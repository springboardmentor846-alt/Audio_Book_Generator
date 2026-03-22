import subprocess
import os

def text_to_speech(text, voice_gender="Female", slow=False, output_file="output.mp3"):
    # edge-tts supports long text, but we can limit or just pass it directly
    # To avoid command line length limits on Windows, let's write text to a temp file
    temp_txt = "temp_input.txt"
    with open(temp_txt, "w", encoding="utf-8") as f:
        f.write(text)

    voice = "en-US-ChristopherNeural" if voice_gender == "Male" else "en-US-JennyNeural"
    rate = "-30%" if slow else "+0%"

    command = [
        "edge-tts",
        "--voice", voice,
        "--rate", rate,
        "-f", temp_txt,
        "--write-media", output_file
    ]

    try:
        subprocess.run(command, check=True)
    except Exception as e:
        print("TTS Error:", e)
    finally:
        if os.path.exists(temp_txt):
            os.remove(temp_txt)

    return output_file