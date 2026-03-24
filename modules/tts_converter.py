from gtts import gTTS
import uuid
import os

def text_to_speech(text):

    if not text.strip():
        return None

    # create outputs folder if not exists
    os.makedirs("outputs", exist_ok=True)

    filename = f"outputs/{uuid.uuid4()}.mp3"

    tts = gTTS(text=text, lang="en")

    tts.save(filename)

    return filename
