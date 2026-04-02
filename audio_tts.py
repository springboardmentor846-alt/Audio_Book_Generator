import asyncio
import os
import re
import uuid
from typing import TYPE_CHECKING

import edge_tts
import streamlit as st

if TYPE_CHECKING:
    
    from pydub import AudioSegment


voice_map = {
    "English": {
        "Female": "en-US-AriaNeural",  
        "Male": "en-US-GuyNeural",  
    },
    "Hindi": {
        "Female": "hi-IN-SwaraNeural",
        "Male": "hi-IN-MadhurNeural",
    },
    "Marathi": {
        "Female": "mr-IN-AarohiNeural",
        "Male": "mr-IN-ManoharNeural",
    },
}


TTS_RATE = "-4%"  
TTS_PITCH = "-2Hz"  


def get_voice_for_settings(language: str, gender: str) -> str:
    """
    Resolve the Edge TTS voice name from selected language and gender.
    Falls back gracefully if a combination is missing.
    """
    lang_map = voice_map.get(language, {})
    if isinstance(lang_map, dict):
        if gender in lang_map:
            return lang_map[gender]
        if "Female" in lang_map:
            return lang_map["Female"]
        if lang_map:
            return next(iter(lang_map.values()))
    default_map = voice_map.get("English", {})
    if isinstance(default_map, dict) and "Female" in default_map:
        return default_map["Female"]
    return "en-US-AriaNeural"


def _split_into_sentences(text: str, max_chars: int = 400) -> list[str]:
    """
    Split text into sentence-like chunks for more natural TTS, avoiding very
    long monotone runs.
    """
    if not text or len(text) <= max_chars:
        return [text] if text and text.strip() else []

    chunks: list[str] = []
    parts = re.split(r"(?<=[.!?])\s+", text)
    current = ""
    for p in parts:
        if len(current) + len(p) + 1 <= max_chars:
            current = (current + " " + p).strip() if current else p
        else:
            if current:
                chunks.append(current)
            current = (
                p if len(p) <= max_chars else p[:max_chars].rsplit(" ", 1)[0] or p[:max_chars]
            )
    if current:
        chunks.append(current)
    return chunks


async def _tts_chunk(chunk: str, voice: str, rate: str, pitch: str, out_path: str) -> None:
    """
    Render a single text chunk to an MP3 file using Edge TTS.
    """
    comm = edge_tts.Communicate(chunk, voice, rate=rate, pitch=pitch)
    await comm.save(out_path)


async def _speech_to_audiosegment(
    text: str,
    voice: str,
    rate: str = TTS_RATE,
    pitch: str = TTS_PITCH,
) -> "AudioSegment":
    """
    Convert a speech-only text segment into an AudioSegment, using the same
    sentence-level chunking strategy as before.
    """
    from pydub import AudioSegment  

    chunks = _split_into_sentences(text, max_chars=350)
    if not chunks:
        chunks = [text.strip()]

    temp_files: list[str] = []
    for chunk in chunks:
        if not chunk.strip():
            continue
        path = f"audiobook_speech_{uuid.uuid4().hex}.mp3"
        await _tts_chunk(chunk, voice, rate, pitch, path)
        temp_files.append(path)

    
    combined = AudioSegment.empty()
    for path in temp_files:
        combined += AudioSegment.from_mp3(path)
        try:
            os.remove(path)
        except Exception:  
            pass

    return combined


async def edge_text_to_audio_natural(
    text: str,
    voice: str,
    rate: str = TTS_RATE,
    pitch: str = TTS_PITCH,
) -> str | None:
    """
    Convert full narration text into a single MP3 file using sentence-level
    chunking. Bracketed sound cues are removed before generating audio.
    """
    if not text or not text.strip():
        return None

    
    stripped = re.sub(r"\(.*?\)", "", text).strip()
    if not stripped:
        return None

    try:
        from pydub import AudioSegment  
    except ImportError:
        
        output_file = f"audiobook_{uuid.uuid4().hex}.mp3"
        comm = edge_tts.Communicate(stripped, voice, rate=rate, pitch=pitch)
        await comm.save(output_file)
        return output_file

    speech_audio = await _speech_to_audiosegment(stripped, voice, rate, pitch)

    
    if len(speech_audio) == 0:
        return None

    output_file = f"audiobook_{uuid.uuid4().hex}.mp3"
    speech_audio.export(output_file, format="mp3")
    return output_file


def generate_audio_file(text: str, voice: str, rate: str = TTS_RATE, pitch: str = TTS_PITCH) -> str | None:
    """
    Public entrypoint for the app:
    - Accepts full narration text (may contain bracketed sound cues),
    - Returns path to the final mixed MP3 file.
    """
    try:
        return asyncio.run(edge_text_to_audio_natural(text, voice, rate, pitch))
    except Exception as e:  
        st.error(f"Error generating audio: {str(e)}")
        return None

