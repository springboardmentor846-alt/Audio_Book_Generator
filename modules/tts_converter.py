from gtts import gTTS
import uuid
import os

def text_to_speech(text, lang="en", prefix="audio"):

    if not text.strip():
        return None

    os.makedirs("outputs", exist_ok=True)

    filename = f"outputs/{prefix}_{uuid.uuid4()}.mp3"

    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

    return filename