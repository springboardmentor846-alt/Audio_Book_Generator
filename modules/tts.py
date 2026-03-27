from gtts import gTTS
import io
from concurrent.futures import ThreadPoolExecutor


def split_text(text, max_chars=6000):

    words = text.split()
    chunks = []
    current = ""

    for word in words:

        if len(current) + len(word) < max_chars:
            current += " " + word
        else:
            chunks.append(current)
            current = word

    if current:
        chunks.append(current)

    return chunks


# ---------- GENERATE SINGLE AUDIO CHUNK ----------
def generate_chunk(chunk):

    temp_audio = io.BytesIO()

    tts = gTTS(text=chunk, lang="en", slow=False)

    tts.write_to_fp(temp_audio)

    temp_audio.seek(0)

    return temp_audio.read()


# ---------- MAIN TTS FUNCTION ----------
def text_to_speech(text):

    chunks = split_text(text)

    audio_bytes = io.BytesIO()

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(generate_chunk, chunks)

    for audio in results:
        audio_bytes.write(audio)

    audio_bytes.seek(0)

    return audio_bytes