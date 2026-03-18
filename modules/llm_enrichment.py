import json
import re

from modules.llm_auto import call_llm_auto

def enrich_text_standard(text: str) -> str:
    from modules.extractor import chunk_text

    chunks = chunk_text(text, max_chars=3500)
    enriched_parts = []

    for chunk in chunks:
        prompt = _build_standard_prompt(chunk)
        enriched_parts.append(call_llm_auto(prompt))

    return "\n\n".join(enriched_parts)


def enrich_text_dramatized(text: str) -> dict:
    """
    Analyse the text and return a structured dramatized script as a dict:

    {
        "title": str,
        "scenes": [
            {
                "scene_type": "narration" | "dialogue",
                "character":  "NARRATOR" | <character name>,
                "emotion":    "neutral" | "happy" | "sad" | "tense" |
                              "excited" | "angry" | "fearful" | "mysterious",
                "rate":       e.g. "+10%",
                "pitch":      e.g. "+2Hz",
                "text":       str
            },
            ...
        ]
    }
    """
    from modules.extractor import chunk_text

    chunks = chunk_text(text, max_chars=3000)
    all_scenes: list[dict] = []
    title = "Chapter"

    for chunk in chunks:
        prompt = _build_dramatized_prompt(chunk)
        raw_response = call_llm_auto(prompt)
        parsed = _parse_dramatized_response(raw_response, fallback_text=chunk)
        if not title or title == "Chapter":
            title = parsed.get("title", "Chapter")
        all_scenes.extend(parsed.get("scenes", []))

    return {"title": title, "scenes": all_scenes}

def _build_standard_prompt(text: str) -> str:
    return f"""You are an expert audiobook narrator and writer. Rewrite the following text for an engaging audiobook narration.

Guidelines:
- Use a warm, engaging narrative voice suitable for listening
- Break overly long sentences for natural spoken flow
- Use ellipsis (...) sparingly to indicate natural pauses
- Remove formatting artifacts such as page numbers, headers, and footnote markers
- Preserve all factual information and the original meaning exactly
- IMPORTANT: Detect the language of the source text and rewrite entirely in that same language. Do NOT translate.
- Do NOT add fictional content or information not present in the source

Text to rewrite:
{text}

Provide ONLY the rewritten narration text in the original language. No commentary or explanation."""


def _build_dramatized_prompt(text: str) -> str:
    return f"""You are an expert audiobook producer creating a fully dramatized audio script.

Analyse the text below and transform it into a structured dramatized script. Return a JSON object with this EXACT structure (no markdown, no code fences, pure JSON):

{{
  "title": "inferred title or section name",
  "scenes": [
    {{
      "scene_type": "narration",
      "character": "NARRATOR",
      "emotion": "neutral",
      "rate": "+0%",
      "pitch": "+0Hz",
      "text": "scene text here"
    }},
    {{
      "scene_type": "dialogue",
      "character": "CHARACTER NAME",
      "emotion": "excited",
      "rate": "+15%",
      "pitch": "+5Hz",
      "text": "dialogue text here"
    }}
  ]
}}

Rules:
- scene_type is "narration" for descriptive prose and "dialogue" for spoken lines
- character is "NARRATOR" for narration; use the actual character name for dialogue
- emotion must be one of: neutral, happy, sad, tense, excited, angry, fearful, mysterious
- rate adjusts speaking speed: use "-10%" to "-30%" for slow/sad, "+10%" to "+30%" for fast/excited
- pitch adjusts voice pitch: use "-5Hz" to "-10Hz" for sad/dark, "+3Hz" to "+8Hz" for happy/excited
- Keep each scene segment to 1-4 sentences for natural pacing
- Extract ALL characters mentioned speaking in the text
- IMPORTANT: Detect the language of the source text and write ALL "text" field values in that same language. Do NOT translate.

Source text:
{text}

Return ONLY valid JSON."""



def _parse_dramatized_response(raw: str, fallback_text: str) -> dict:
    """Parse LLM JSON response; fall back to a simple narration if invalid."""
    # Strip markdown code fences if present
    cleaned = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()

    try:
        data = json.loads(cleaned)
        if "scenes" in data and isinstance(data["scenes"], list) and data["scenes"]:
            return data
    except (json.JSONDecodeError, KeyError):
        pass

    # Fallback: wrap the raw response text as a single narration scene
    return {
        "title": "Chapter",
        "scenes": [
            {
                "scene_type": "narration",
                "character": "NARRATOR",
                "emotion": "neutral",
                "rate": "+0%",
                "pitch": "+0Hz",
                "text": raw if raw.strip() else fallback_text,
            }
        ],
    }
