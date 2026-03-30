import json
import os
from datetime import datetime
from pathlib import Path

ANALYTICS_FILE = Path("output/analytics.json")

def _load() -> list:
    if ANALYTICS_FILE.exists():
        with open(ANALYTICS_FILE, "r") as f:
            return json.load(f)
    return []

def _save(data: list):
    ANALYTICS_FILE.parent.mkdir(exist_ok=True)
    with open(ANALYTICS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_generation(files: list[str], char_count: int, llm_used: bool, model: str | None, duration_sec: float):
    """Log a single audiobook generation event."""
    data = _load()
    data.append({
        "timestamp": datetime.now().isoformat(),
        "files": files,
        "char_count": char_count,
        "llm_used": llm_used,
        "model": model,
        "duration_sec": round(duration_sec, 2)
    })
    _save(data)

def get_all_records() -> list:
    """Return raw list of all logged records."""
    return _load()

def get_summary() -> dict:
    """Return aggregated analytics summary."""
    data = _load()
    if not data:
        return {"total_runs": 0}

    total_chars = sum(r["char_count"] for r in data)
    llm_runs = sum(1 for r in data if r["llm_used"])
    avg_duration = sum(r["duration_sec"] for r in data) / len(data)

    model_counts = {}
    for r in data:
        m = r["model"] or "none"
        model_counts[m] = model_counts.get(m, 0) + 1

    return {
        "total_runs": len(data),
        "total_chars_processed": total_chars,
        "llm_enhanced_runs": llm_runs,
        "avg_duration_sec": round(avg_duration, 2),
        "model_usage": model_counts,
        "last_run": data[-1]["timestamp"]
    }
