import edge_tts
import asyncio
import tempfile

async def _generate(text, voice):
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(temp_audio.name)
    return temp_audio.name

def generate_audio(text, voice_type="female"):
    if voice_type == "male":
        voice = "en-US-GuyNeural"
    else:
        voice = "en-US-JennyNeural"

    return asyncio.run(_generate(text, voice))