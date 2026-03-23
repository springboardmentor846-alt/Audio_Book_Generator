from io import BytesIO
import asyncio
import re
from typing import Callable, Optional

try:
    import edge_tts
except ImportError:
    edge_tts = None  # type: ignore[assignment]

try:
    from pydub import AudioSegment  # type: ignore[import]
except Exception:
    AudioSegment = None  # type: ignore[assignment]


# Voice options: label -> edge-tts voice ID (region before gender)
VOICE_OPTIONS: dict[str, str] = {
    "US Male": "en-US-GuyNeural",
    "US Female": "en-US-JennyNeural",
    "British Male": "en-GB-RyanNeural",
    "British Female": "en-GB-SoniaNeural",
    "Indian Male": "en-IN-PrabhatNeural",
    "Indian Female": "en-IN-NeerjaNeural",
    "Hindi Male": "hi-IN-MadhurNeural",
    "Hindi Female": "hi-IN-SwaraNeural",
    "Child": "en-US-AnaNeural",
}

DEFAULT_VOICE = "en-US-JennyNeural"

# edge-tts works well with chunks up to ~5000 chars; we use 2000 to be safe
EDGE_TTS_MAX_CHARS = 2000


def _split_text_for_tts(text: str, *, max_chars: int = EDGE_TTS_MAX_CHARS) -> list[str]:
    """
    Split long text into chunks safe for TTS (edge-tts has per-request limits).
    """
    t = (text or "").strip()
    if not t:
        return []

    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", t) if p.strip()]

    chunks: list[str] = []
    cur = ""

    def flush() -> None:
        nonlocal cur
        if cur.strip():
            chunks.append(cur.strip())
        cur = ""

    def add_piece(piece: str) -> None:
        nonlocal cur
        piece = piece.strip()
        if not piece:
            return
        candidate = piece if not cur else f"{cur}\n\n{piece}"
        if len(candidate) <= max_chars:
            cur = candidate
            return
        flush()
        if len(piece) <= max_chars:
            cur = piece
            return
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", piece) if s.strip()]
        if not sentences:
            for i in range(0, len(piece), max_chars):
                chunks.append(piece[i : i + max_chars].strip())
            return
        tmp = ""
        for s in sentences:
            cand = s if not tmp else f"{tmp} {s}"
            if len(cand) <= max_chars:
                tmp = cand
            else:
                if tmp:
                    chunks.append(tmp.strip())
                tmp = s
                if len(tmp) > max_chars:
                    for i in range(0, len(tmp), max_chars):
                        chunks.append(tmp[i : i + max_chars].strip())
                    tmp = ""
        if tmp:
            chunks.append(tmp.strip())

    for p in paragraphs:
        add_piece(p)
    flush()
    return chunks


async def _generate_chunk_async(text: str, voice_id: str) -> bytes:
    """Generate MP3 bytes for one chunk using edge-tts."""
    out = BytesIO()
    communicate = edge_tts.Communicate(text, voice_id)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            out.write(chunk["data"])
    return out.getvalue()


def text_to_speech(
    text: str,
    voice: str = "US Female",
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> BytesIO:
    """
    Convert text to speech using edge-tts and return an in-memory MP3 file.

    Parameters
    ----------
    text:
        The input text to convert to speech.
    voice:
        Voice label: one of US Male, US Female, British Male, British Female,
        Indian Male, Indian Female, Child.
    progress_callback:
        Optional callback(done_chunks, total_chunks) for progress.
    """
    if not text.strip():
        raise ValueError("Empty text provided to text_to_speech.")

    if edge_tts is None:
        raise RuntimeError(
            "edge-tts is not installed. Install it with: pip install edge-tts"
        )

    voice_id = VOICE_OPTIONS.get(voice, DEFAULT_VOICE)
    chunks = _split_text_for_tts(text, max_chars=EDGE_TTS_MAX_CHARS)
    if not chunks:
        raise ValueError("Empty text provided to text_to_speech.")

    total = len(chunks)
    segment_bytes_list: list[bytes] = []

    async def run_all() -> None:
        nonlocal segment_bytes_list
        for idx, chunk in enumerate(chunks, start=1):
            data = await _generate_chunk_async(chunk, voice_id)
            segment_bytes_list.append(data)
            if progress_callback is not None:
                try:
                    progress_callback(idx, total)
                except Exception:
                    pass

    asyncio.run(run_all())

    if not segment_bytes_list:
        raise ValueError("No audio generated.")

    if AudioSegment is not None and len(segment_bytes_list) > 1:
        combined = AudioSegment.empty()
        for data in segment_bytes_list:
            combined += AudioSegment.from_mp3(BytesIO(data))
        out = BytesIO()
        combined.export(out, format="mp3")
        out.seek(0)
        return out

    out = BytesIO()
    for data in segment_bytes_list:
        out.write(data)
    out.seek(0)
    return out
