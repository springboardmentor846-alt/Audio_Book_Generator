import pyttsx3
import os
import uuid
from gtts import gTTS

OUTPUT_DIR = "outputs"

def text_to_speech(text, rate=180, volume=1.0, language="en"):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filename = f"audiobook_{uuid.uuid4().hex}.mp3"
    file_path = os.path.join(OUTPUT_DIR, filename)

    if language == "en":
        engine = pyttsx3.init()
        engine.setProperty("rate", rate)
        engine.setProperty("volume", volume)

        engine.save_to_file(text, file_path)
        engine.runAndWait()
    else:
        tts = gTTS(text=text, lang=language)
        tts.save(file_path)

    return file_path   # ✅ FIXED