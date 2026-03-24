"""
Ambient Soundscape Mixer — procedurally generates emotion-matched ambient audio
and mixes it under each TTS segment at a configurable volume.

Algorithm
---------
1. Generate pink (1/f) noise via FFT frequency-domain shaping.
2. Bandpass-filter to an emotion-specific frequency range.
3. Apply optional tremolo (amplitude modulation) for tense/fearful/mysterious tones.
4. Fade in/out to avoid clicks at segment boundaries.
5. Scale to the requested dBFS volume and overlay onto the TTS segment with pydub.

Requires: numpy, pydub (both in requirements.txt)
"""

import os
import numpy as np

# ── Emotion → (low_hz, high_hz, mod_rate_hz, mod_depth) ──────────────────────
# low/high_hz  : bandpass window that gives each emotion its timbral character
# mod_rate_hz  : tremolo rate (0 = no tremolo)
# mod_depth    : tremolo depth 0-1 (fraction of amplitude swing)
_SOUNDSCAPE_PARAMS: dict[str, tuple[float, float, float, float]] = {
    "neutral":    (200.0, 1200.0, 0.0,  0.00),   # soft mid-range presence
    "happy":      (500.0, 3000.0, 0.0,  0.00),   # airy, bright
    "excited":    (600.0, 4000.0, 2.0,  0.15),   # bright + fast shimmer
    "sad":        (60.0,  350.0,  0.0,  0.00),   # dark, low rumble
    "mysterious": (50.0,  280.0,  0.3,  0.28),   # very dark, slow pulse
    "tense":      (55.0,  230.0,  4.5,  0.22),   # deep rumble, rapid pulse
    "angry":      (70.0,  320.0,  5.0,  0.18),   # low-mid crunch, fast pulse
    "fearful":    (45.0,  260.0,  0.8,  0.32),   # sub-bass, slow deep throb
}
_DEFAULT_PARAMS = _SOUNDSCAPE_PARAMS["neutral"]

_SAMPLE_RATE = 22050   # Hz — good quality, half the standard 44.1k for speed
_FADE_SECS   = 0.4     # fade in/out per segment to avoid clicks


# ── Public API ────────────────────────────────────────────────────────────────

def mix_ambience_for_scenes(
    audio_files: list[str],
    scenes: list[dict],
    volume_db: float = -22.0,
) -> list[str]:
    """
    For every TTS segment file, generate matching ambient audio based on the
    scene's emotion and mix it in at `volume_db` dBFS. Files are overwritten
    in-place. Returns the same list of paths (unchanged).
    """
    for path in audio_files:
        try:
            idx     = _scene_index_from_path(path)
            emotion = scenes[idx].get("emotion", "neutral") if idx < len(scenes) else "neutral"
            _mix_segment(path, emotion, volume_db)
        except Exception as e:
            # Never let a soundscape error break TTS delivery
            print(f"[Soundscape] Skipped {os.path.basename(path)}: {e}")
    return audio_files


# ── Internal helpers ──────────────────────────────────────────────────────────

def _scene_index_from_path(path: str) -> int:
    """Extract scene index from a filename like 'seg_0003.mp3' → 3."""
    stem = os.path.splitext(os.path.basename(path))[0]   # 'seg_0003'
    return int(stem.split("_")[1])


def _mix_segment(path: str, emotion: str, volume_db: float) -> None:
    """Generate ambient audio and overlay it onto the TTS segment in-place."""
    from pydub import AudioSegment

    tts = AudioSegment.from_mp3(path)
    duration_ms = len(tts)
    if duration_ms < 300:
        return  # too short to add meaningful ambience

    ambient = _generate_ambient(emotion, duration_ms, volume_db)

    # Match channels and sample-rate to TTS audio
    if ambient.channels != tts.channels:
        ambient = ambient.set_channels(tts.channels)
    if ambient.frame_rate != tts.frame_rate:
        ambient = ambient.set_frame_rate(tts.frame_rate)

    mixed = tts.overlay(ambient)
    mixed.export(path, format="mp3")


def _generate_ambient(
    emotion: str,
    duration_ms: int,
    volume_db: float,
) -> "AudioSegment":
    """Build a procedural ambient AudioSegment for the given emotion and length."""
    from pydub import AudioSegment

    low_hz, high_hz, mod_rate, mod_depth = _SOUNDSCAPE_PARAMS.get(
        emotion.lower(), _DEFAULT_PARAMS
    )
    n = int(_SAMPLE_RATE * duration_ms / 1000)

    # 1. Pink (1/f) noise — far more natural-sounding than white noise
    signal = _pink_noise(n)

    # 2. Bandpass to emotion-specific frequency window
    signal = _bandpass_fft(signal, low_hz, high_hz)

    # 3. Tremolo (amplitude modulation) for tense / fearful / mysterious
    if mod_rate > 0.0 and mod_depth > 0.0:
        t = np.linspace(0.0, duration_ms / 1000.0, n, endpoint=False, dtype=np.float32)
        lfo = 1.0 - mod_depth * (0.5 + 0.5 * np.sin(2.0 * np.pi * mod_rate * t))
        signal *= lfo

    # 4. Fade in / out to prevent click artefacts at segment edges
    fade_n = min(int(_SAMPLE_RATE * _FADE_SECS), n // 4)
    if fade_n > 0:
        signal[:fade_n]  *= np.linspace(0.0, 1.0, fade_n, dtype=np.float32)
        signal[-fade_n:] *= np.linspace(1.0, 0.0, fade_n, dtype=np.float32)

    # 5. Normalise peak → apply target dBFS gain → convert to int16 PCM
    peak = float(np.max(np.abs(signal))) or 1e-9
    gain = 10.0 ** (volume_db / 20.0)
    pcm  = (signal / peak * gain * 32767.0).clip(-32767, 32767).astype(np.int16)

    return AudioSegment(
        data=pcm.tobytes(),
        sample_width=2,          # 16-bit
        frame_rate=_SAMPLE_RATE,
        channels=1,
    )


def _pink_noise(n: int) -> np.ndarray:
    """
    Generate pink (1/f) noise of length n via FFT frequency-shaping.
    Each frequency bin is scaled by 1/sqrt(f) to produce the 1/f power spectrum.
    """
    rng   = np.random.default_rng()
    white = rng.standard_normal(n).astype(np.float32)
    fft   = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n).astype(np.float32)
    freqs[0] = 1e-9                  # avoid DC divide-by-zero
    fft /= np.sqrt(freqs)
    return np.fft.irfft(fft, n=n).astype(np.float32)


def _bandpass_fft(signal: np.ndarray, low_hz: float, high_hz: float) -> np.ndarray:
    """Zero-phase brick-wall FFT bandpass filter."""
    n     = len(signal)
    fft   = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(n, d=1.0 / _SAMPLE_RATE).astype(np.float32)
    fft[freqs < low_hz]  = 0.0
    fft[freqs > high_hz] = 0.0
    return np.fft.irfft(fft, n=n).astype(np.float32)
