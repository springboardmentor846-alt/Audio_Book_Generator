"""
Auto QA Auditor — detects quality issues in generated audio segments.

Issue types
-----------
  EMPTY        – file missing or < 2 KB  (TTS generation failed)
  TRUNCATED    – audio much shorter than word-count suggests (cut off)
  HALLUCINATED – audio much longer than word-count suggests (LLM padding)
  HIGH_SILENCE – > 70 % of audio is silence (clipping / TTS glitch)
"""

import os
from dataclasses import dataclass
from typing import Optional

# ── Thresholds ────────────────────────────────────────────────────────────────
_WORDS_PER_SECOND   = 2.5   # typical Edge TTS speaking rate
_MIN_FILE_BYTES     = 2048  # < 2 KB → treat as empty / failed
_SILENCE_THRESH_DB  = -50   # dBFS level considered "silent"
_MAX_SILENCE_RATIO  = 0.70  # flag if > 70 % of audio is silence
_TRUNCATED_RATIO    = 0.40  # flag if actual < 40 % of expected duration
_HALLUCINATED_RATIO = 2.50  # flag if actual > 250 % of expected duration


@dataclass
class QAIssue:
    segment_index: int
    path: str
    issue_type: str          # EMPTY | TRUNCATED | HALLUCINATED | HIGH_SILENCE
    severity: str            # error | warning
    details: str
    expected_duration: Optional[float] = None
    actual_duration: Optional[float] = None


def audit_segments(segment_paths: list[str], texts: list[str]) -> list[QAIssue]:
    """Audit multiple audio segments against their source texts."""
    issues: list[QAIssue] = []
    for idx, (path, text) in enumerate(zip(segment_paths, texts)):
        issues.extend(_audit_one(idx, path, text))
    return issues


def audit_single_file(path: str, text: str) -> list[QAIssue]:
    """Audit a single audio file (standard mode — whole file as one segment)."""
    return _audit_one(0, path, text)


# ── Internal helpers ──────────────────────────────────────────────────────────

def _audit_one(idx: int, path: str, text: str) -> list[QAIssue]:
    issues: list[QAIssue] = []

    # 1. File existence / size ─────────────────────────────────────────────────
    if not os.path.exists(path):
        issues.append(QAIssue(
            segment_index=idx, path=path,
            issue_type="EMPTY", severity="error",
            details="Segment file does not exist — TTS generation failed.",
        ))
        return issues

    size = os.path.getsize(path)
    if size < _MIN_FILE_BYTES:
        issues.append(QAIssue(
            segment_index=idx, path=path,
            issue_type="EMPTY", severity="error",
            details=f"File is only {size} bytes — likely empty or corrupt.",
        ))
        return issues

    # 2. Duration + silence checks (requires pydub) ────────────────────────────
    try:
        from pydub import AudioSegment

        audio       = AudioSegment.from_mp3(path)
        actual_secs = len(audio) / 1000.0
        word_count  = len(text.split())
        exp_secs    = word_count / _WORDS_PER_SECOND if word_count > 0 else 0

        if exp_secs > 0:
            ratio = actual_secs / exp_secs
            if ratio < _TRUNCATED_RATIO:
                issues.append(QAIssue(
                    segment_index=idx, path=path,
                    issue_type="TRUNCATED", severity="error",
                    details=(
                        f"Audio is {actual_secs:.1f}s but ~{exp_secs:.1f}s expected "
                        f"for {word_count} words ({ratio:.0%} of expected). "
                        "Likely cut off mid-sentence."
                    ),
                    expected_duration=exp_secs,
                    actual_duration=actual_secs,
                ))
            elif ratio > _HALLUCINATED_RATIO:
                issues.append(QAIssue(
                    segment_index=idx, path=path,
                    issue_type="HALLUCINATED", severity="warning",
                    details=(
                        f"Audio is {actual_secs:.1f}s but ~{exp_secs:.1f}s expected "
                        f"for {word_count} words ({ratio:.0%} of expected). "
                        "LLM may have added unrequested content."
                    ),
                    expected_duration=exp_secs,
                    actual_duration=actual_secs,
                ))

        silence_secs  = _measure_silence(audio)
        silence_ratio = silence_secs / actual_secs if actual_secs > 0 else 0
        if silence_ratio > _MAX_SILENCE_RATIO:
            issues.append(QAIssue(
                segment_index=idx, path=path,
                issue_type="HIGH_SILENCE", severity="warning",
                details=(
                    f"{silence_ratio:.0%} of audio is silence "
                    f"({silence_secs:.1f}s / {actual_secs:.1f}s total). "
                    "Possible TTS glitch or clipping."
                ),
                actual_duration=actual_secs,
            ))

    except ImportError:
        pass  # pydub not installed; size-only checks still run
    except Exception:
        pass  # don't crash the audit over one bad segment

    return issues


def _measure_silence(audio, threshold_db: float = _SILENCE_THRESH_DB) -> float:
    """Return total silence duration in seconds for a pydub AudioSegment."""
    try:
        from pydub.silence import detect_silence
        ranges = detect_silence(audio, min_silence_len=200, silence_thresh=threshold_db)
        return sum(end - start for start, end in ranges) / 1000.0
    except Exception:
        return 0.0
