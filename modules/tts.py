from gtts import gTTS
import tempfile
import os

def text_to_speech(text):
    tts = gTTS(text=text, lang="en")

    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)

    return temp_audio.name