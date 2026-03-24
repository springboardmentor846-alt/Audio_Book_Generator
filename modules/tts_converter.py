import asyncio
import os
import re
import shutil


# ---------------------------------------------------------------------------
# Voice configuration
# ---------------------------------------------------------------------------

# Available voices for the UI voice selector
AVAILABLE_VOICES: dict[str, str] = {
    # ── English ──────────────────────────────────────────────────
    "Aria (Female, US English)":         "en-US-AriaNeural",
    "Jenny (Female, US English)":        "en-US-JennyNeural",
    "Guy (Male, US English)":            "en-US-GuyNeural",
    "Brian (Male, US English)":          "en-US-BrianNeural",
    "Emma (Female, US English)":         "en-US-EmmaNeural",
    "Ryan (Male, UK English)":           "en-GB-RyanNeural",
    "Sonia (Female, UK English)":        "en-GB-SoniaNeural",
    "William (Male, AU English)":        "en-AU-WilliamNeural",
    "Neerja (Female, Indian English)":   "en-IN-NeerjaNeural",
    # ── Hindi ────────────────────────────────────────────────────
    "Swara (Female, Hindi)":             "hi-IN-SwaraNeural",
    "Madhur (Male, Hindi)":              "hi-IN-MadhurNeural",
    # ── Tamil ────────────────────────────────────────────────────
    "Pallavi (Female, Tamil)":           "ta-IN-PallaviNeural",
    "Valluvar (Male, Tamil)":            "ta-IN-ValluvarNeural",
    # ── Telugu ───────────────────────────────────────────────────
    "Shruti (Female, Telugu)":           "te-IN-ShrutiNeural",
    "Mohan (Male, Telugu)":              "te-IN-MohanNeural",
    # ── Bengali ──────────────────────────────────────────────────
    "Tanishaa (Female, Bengali)":        "bn-IN-TanishaaNeural",
    "Bashkar (Male, Bengali)":           "bn-IN-BashkarNeural",
    # ── Malayalam ────────────────────────────────────────────────
    "Sobhana (Female, Malayalam)":       "ml-IN-SobhanaNeural",
    "Midhun (Male, Malayalam)":          "ml-IN-MidhunNeural",
    # ── Marathi ──────────────────────────────────────────────────
    "Aarohi (Female, Marathi)":          "mr-IN-AarohiNeural",
    "Manohar (Male, Marathi)":           "mr-IN-ManoharNeural",
    # ── Kannada ──────────────────────────────────────────────────
    "Sapna (Female, Kannada)":           "kn-IN-SapnaNeural",
    "Gagan (Male, Kannada)":             "kn-IN-GaganNeural",
    # ── Gujarati ─────────────────────────────────────────────────
    "Dhwani (Female, Gujarati)":         "gu-IN-DhwaniNeural",
    "Niranjan (Male, Gujarati)":         "gu-IN-NiranjanNeural",
    # ── Urdu ─────────────────────────────────────────────────────
    "Gul (Female, Urdu)":                "ur-IN-GulNeural",
    "Salman (Male, Urdu)":               "ur-IN-SalmanNeural",
}

# Language code → two character voices (male, female) for that language
_LANG_CHARACTER_VOICES: dict[str, list[str]] = {
    "en": [
        "en-US-BrianNeural", "en-US-EmmaNeural",
        "en-GB-RyanNeural",  "en-GB-SoniaNeural",
        "en-AU-WilliamNeural", "en-AU-NatashaNeural",
        "en-CA-LiamNeural",  "en-IN-NeerjaNeural",
    ],
    "hi": ["hi-IN-MadhurNeural", "hi-IN-SwaraNeural"],
    "ta": ["ta-IN-ValluvarNeural", "ta-IN-PallaviNeural"],
    "te": ["te-IN-MohanNeural",   "te-IN-ShrutiNeural"],
    "bn": ["bn-IN-BashkarNeural", "bn-IN-TanishaaNeural"],
    "ml": ["ml-IN-MidhunNeural",  "ml-IN-SobhanaNeural"],
    "mr": ["mr-IN-ManoharNeural", "mr-IN-AarohiNeural"],
    "kn": ["kn-IN-GaganNeural",   "kn-IN-SapnaNeural"],
    "gu": ["gu-IN-NiranjanNeural","gu-IN-DhwaniNeural"],
    "ur": ["ur-IN-SalmanNeural",  "ur-IN-GulNeural"],
}

# Emotions recognised for prosody — anything else falls back to "neutral"
_VALID_EMOTIONS = {
    "neutral", "happy", "sad", "tense",
    "excited", "angry", "fearful", "mysterious",
}

# Default prosody per emotion (rate, pitch)
_EMOTION_PROSODY: dict[str, tuple[str, str]] = {
    "neutral":    ("+0%",  "+0Hz"),
    "happy":      ("+15%", "+5Hz"),
    "excited":    ("+20%", "+8Hz"),
    "sad":        ("-15%", "-5Hz"),
    "fearful":    ("-10%", "-3Hz"),
    "tense":      ("+10%", "-3Hz"),
    "angry":      ("+15%", "-5Hz"),
    "mysterious": ("-10%", "-5Hz"),
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def run_tts_standard(text: str, output_path: str, voice: str = "en-US-AriaNeural") -> str:
    """Convert plain text to a single MP3 file."""
    _run_async(_tts_standard(text, output_path, voice))
    return output_path


def run_tts_dramatized(
    script: dict,
    temp_dir: str,
    final_output: str,
    narrator_voice: str = "en-US-AriaNeural",
    use_ambience: bool = False,
    ambience_volume_db: float = -22.0,
) -> str:
    """
    Convert a dramatized script into a single MP3 file.
    narrator_voice controls which language/voice pool is used for all scenes.
    If use_ambience is True, emotion-matched ambient audio is mixed under each segment.
    """
    audio_files = _run_async(_tts_dramatized(script, temp_dir, narrator_voice))

    if not audio_files:
        raise RuntimeError("No audio segments were generated.")

    if use_ambience:
        from modules.soundscape import mix_ambience_for_scenes
        mix_ambience_for_scenes(audio_files, script.get("scenes", []), ambience_volume_db)

    if len(audio_files) == 1:
        shutil.copy(audio_files[0], final_output)
        return final_output

    return _merge_audio_files(audio_files, final_output)


def regenerate_and_remerge(
    bad_indices: list[int],
    script: dict,
    temp_dir: str,
    final_output: str,
    narrator_voice: str = "en-US-AriaNeural",
    use_ambience: bool = False,
    ambience_volume_db: float = -22.0,
) -> str:
    """
    Re-generate only the bad segments (by scene index), then re-merge
    all segments currently in temp_dir into a new final output file.
    Ambience is re-applied to the regenerated segments if enabled.
    """
    regenerated = _run_async(_regenerate_segments(bad_indices, script, temp_dir, narrator_voice))

    if use_ambience and regenerated:
        from modules.soundscape import mix_ambience_for_scenes
        mix_ambience_for_scenes(regenerated, script.get("scenes", []), ambience_volume_db)

    all_segments = sorted([
        os.path.join(temp_dir, f)
        for f in os.listdir(temp_dir)
        if f.startswith("seg_") and f.endswith(".mp3")
    ])
    if not all_segments:
        raise RuntimeError("No segments found in temp_dir after regeneration.")
    if len(all_segments) == 1:
        shutil.copy(all_segments[0], final_output)
        return final_output
    return _merge_audio_files(all_segments, final_output)


# ---------------------------------------------------------------------------
# Async TTS helpers
# ---------------------------------------------------------------------------

async def _tts_standard(text: str, output_path: str, voice: str) -> None:
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


async def _tts_dramatized(
    script: dict,
    temp_dir: str,
    narrator_voice: str,
) -> list[str]:
    import edge_tts

    # Derive language pool from narrator voice (e.g. "ta" from "ta-IN-PallaviNeural")
    lang = narrator_voice.split("-")[0].lower()
    char_pool = _LANG_CHARACTER_VOICES.get(lang, _LANG_CHARACTER_VOICES["en"])

    scenes = script.get("scenes", [])
    character_voices = _assign_character_voices(scenes, char_pool, narrator_voice)

    tasks = []
    paths = []

    for i, scene in enumerate(scenes):
        text = scene.get("text", "").strip()
        if not text:
            continue

        character = scene.get("character", "NARRATOR")
        emotion = scene.get("emotion", "neutral").lower()

        # Normalise unknown emotions to neutral
        if emotion not in _VALID_EMOTIONS:
            emotion = "neutral"

        # Rate & pitch: use LLM values if valid, else use emotion defaults
        default_rate, default_pitch = _EMOTION_PROSODY[emotion]
        rate  = _sanitize_rate(scene.get("rate",  default_rate),  default_rate)
        pitch = _sanitize_pitch(scene.get("pitch", default_pitch), default_pitch)

        # Voice selection — narrator always uses the user-selected voice
        voice = narrator_voice if character == "NARRATOR" else character_voices.get(character, narrator_voice)

        segment_path = os.path.join(temp_dir, f"seg_{i:04d}.mp3")
        paths.append(segment_path)

        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        tasks.append(communicate.save(segment_path))

    # return_exceptions=True prevents one bad segment from killing all others
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Log any individual segment failures (don't crash the whole generation)
    for idx, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"[TTS] Segment {idx} failed: {result}")

    return [p for p in paths if os.path.exists(p)]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _assign_character_voices(
    scenes: list,
    pool: list[str],
    narrator_voice: str,
) -> dict[str, str]:
    """Map each unique non-narrator character to a distinct voice from the pool."""
    voice_map: dict[str, str] = {}
    idx = 0
    for scene in scenes:
        char = scene.get("character", "NARRATOR")
        if char != "NARRATOR" and char not in voice_map:
            # Cycle through pool, skip narrator_voice so characters sound distinct
            while True:
                candidate = pool[idx % len(pool)]
                idx += 1
                if candidate != narrator_voice or len(pool) == 1:
                    voice_map[char] = candidate
                    break
    return voice_map


def _sanitize_rate(value: str, default: str) -> str:
    """Ensure rate is in edge-tts format: +10% or -10%"""
    v = str(value).strip()
    if re.fullmatch(r"[+-]\d+(\.\d+)?%", v):
        return v
    # Try to extract a number and rebuild
    m = re.search(r"([+-]?\d+(?:\.\d+)?)", v)
    if m:
        num = float(m.group(1))
        return f"{num:+.0f}%"
    return default


def _sanitize_pitch(value: str, default: str) -> str:
    """Ensure pitch is in edge-tts format: +10Hz or -10Hz (case-insensitive input)"""
    v = str(value).strip()
    # Normalise Hz casing
    v_norm = re.sub(r"(?i)hz$", "Hz", v)
    if re.fullmatch(r"[+-]\d+(\.\d+)?Hz", v_norm):
        return v_norm
    # Try to extract a number and rebuild
    m = re.search(r"([+-]?\d+(?:\.\d+)?)", v)
    if m:
        num = float(m.group(1))
        return f"{num:+.0f}Hz"
    return default


def _merge_audio_files(audio_files: list[str], output_path: str) -> str:
    """
    Merge MP3 segments into one file.
    Tries pydub (needs ffmpeg) first; falls back to raw binary concatenation.
    """
    try:
        from pydub import AudioSegment
        combined = AudioSegment.empty()
        pause = AudioSegment.silent(duration=400)
        for path in audio_files:
            try:
                combined += AudioSegment.from_mp3(path) + pause
            except Exception:
                continue
        combined.export(output_path, format="mp3")
        return output_path
    except Exception:
        # Fallback: raw binary concatenation — no ffmpeg needed
        with open(output_path, "wb") as out:
            for path in audio_files:
                try:
                    with open(path, "rb") as f:
                        out.write(f.read())
                except Exception:
                    continue
        return output_path


async def _regenerate_segments(
    bad_indices: list[int],
    script: dict,
    temp_dir: str,
    narrator_voice: str,
) -> list[str]:
    """Re-run TTS for specific scene indices, overwriting their segment files."""
    import edge_tts

    lang        = narrator_voice.split("-")[0].lower()
    char_pool   = _LANG_CHARACTER_VOICES.get(lang, _LANG_CHARACTER_VOICES["en"])
    scenes      = script.get("scenes", [])
    char_voices = _assign_character_voices(scenes, char_pool, narrator_voice)

    tasks, paths = [], []
    for i in bad_indices:
        if i >= len(scenes):
            continue
        scene = scenes[i]
        text  = scene.get("text", "").strip()
        if not text:
            continue

        character = scene.get("character", "NARRATOR")
        emotion   = scene.get("emotion", "neutral").lower()
        if emotion not in _VALID_EMOTIONS:
            emotion = "neutral"

        default_rate, default_pitch = _EMOTION_PROSODY[emotion]
        rate  = _sanitize_rate(scene.get("rate",  default_rate),  default_rate)
        pitch = _sanitize_pitch(scene.get("pitch", default_pitch), default_pitch)
        voice = narrator_voice if character == "NARRATOR" else char_voices.get(character, narrator_voice)

        seg_path = os.path.join(temp_dir, f"seg_{i:04d}.mp3")
        paths.append(seg_path)
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        tasks.append(communicate.save(seg_path))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for idx, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"[TTS] Regen of segment {bad_indices[idx]} failed: {result}")

    return [p for p in paths if os.path.exists(p)]


def _run_async(coro):
    """Run an async coroutine from synchronous code safely."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, coro)
                return future.result()
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)
