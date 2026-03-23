from __future__ import annotations
import re
from typing import Optional
from llm_service import call_llm, is_gemini_available

def clean_text_with_gemini(
    text: str,
    *,
    api_key: Optional[str] = None,
    model_name: str = "gemini-2.0-flash",
) -> tuple[str, str]:
    """Use an LLM (Gemini/Groq) to clean text via llm_service."""
    prompt = (
        "You will receive raw text. This could be a document, speech, or even song lyrics. "
        "Fix obvious OCR errors, but preserve artistic formatting, stanzas, and paragraphs. "
        "Do NOT summarize. Return only the cleaned text.\n\n"
        f"Text:\n{text}"
    )
    
    result, source = call_llm(prompt, api_key=api_key, model_name=model_name, temperature=0.2)
    if result:
        return result, source

    # Fallback: basic cleaning
    return clean_text_basic(text), "basic"


def clean_text_basic(text: str) -> str:
    """Basic text cleaning using regex."""
    if not text: return ""
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


_BASIC_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "else", "when", "while", "for", "to", "of", "in", "on",
    "at", "by", "with", "from", "as", "is", "are", "was", "were", "be", "been", "being", "it", "this", "that",
    "these", "those", "i", "you", "he", "she", "we", "they", "them", "his", "her", "their", "our", "your",
    "not", "no", "yes", "do", "does", "did", "doing", "have", "has", "had", "having", "can", "could", "will",
    "would", "may", "might", "must", "should", "so", "such", "than", "too", "very",
}

def summarize_text_basic(text: str, *, target_word_count: int = 250) -> str:
    """Lightweight extractive summarization."""
    t = clean_text_basic(text)
    if not t: return ""
    words = t.split()
    original_word_count = len(words)
    
    if target_word_count >= original_word_count:
        target_word_count = max(1, int(original_word_count * 0.8))

    if len(t) > 250_000: t = f"{t[:200_000]}\n\n{t[-50_000:]}"

    target_word_count = max(1, min(2500, int(target_word_count)))
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", t) if s.strip()]
    if len(sentences) <= 3: return " ".join(words[:target_word_count]).strip()

    tokens = re.findall(r"[A-Za-z0-9']+", t.lower())
    freqs: dict[str, int] = {}
    for w in tokens:
        if len(w) > 2 and w not in _BASIC_STOPWORDS:
            freqs[w] = freqs.get(w, 0) + 1
    if not freqs: return " ".join(words[:target_word_count]).strip()

    max_f = max(freqs.values())
    for k in freqs: freqs[k] /= max_f

    scored: list[tuple[float, int, str]] = []
    for idx, s in enumerate(sentences):
        stoks = re.findall(r"[A-Za-z0-9']+", s.lower())
        if not stoks: continue
        score_val: float = sum(freqs.get(w, 0.0) for w in stoks)
        score_val *= (1.0 + (0.35 * (1.0 - (idx / max(1, len(sentences) - 1)))))
        scored.append((score_val, idx, s))

    scored.sort(key=lambda x: x[0], reverse=True)
    chosen: list[tuple[int, str]] = []
    wc = 0
    for _, idx, s in scored:
        s_wc = len(s.split())
        if wc + s_wc > target_word_count and wc >= int(target_word_count * 0.6): continue
        chosen.append((idx, s))
        wc += s_wc
        if wc >= target_word_count: break

    chosen.sort(key=lambda x: x[0])
    summary = " ".join(s for _, s in chosen).strip()
    return summary or " ".join(words[:target_word_count]).strip()


def summarize_text_with_gemini(
    text: str,
    *,
    api_key: Optional[str] = None,
    model_name: str = "gemini-2.0-flash",
    target_word_count: int = 250,
) -> tuple[str, str]:
    """Summarize text via llm_service."""
    t = (text or "").strip()
    if not t: return "", "empty"
    
    original_word_count = len(t.split())
    if target_word_count >= original_word_count:
        target_word_count = max(1, int(original_word_count * 0.8))
        
    if original_word_count <= 10:
        return t, "original"

    prompt = (
        "You will receive text from a document. Create a concise, spoken-friendly summary. "
        f"Target strictly less than {original_word_count} words, ideally about {int(target_word_count)} words. "
        "Keep key facts, names, and numbers. Do not use markdown, headings, or bullet symbols. "
        "Return only plain text.\n\n"
        f"Text:\n{t}"
    )

    result, source = call_llm(prompt, api_key=api_key, model_name=model_name, temperature=0.3)
    if result:
        return result, source

    return summarize_text_basic(t, target_word_count=target_word_count), "basic"


def generate_questions_with_gemini(
    text: str,
    *,
    api_key: Optional[str] = None,
    model_name: str = "gemini-2.0-flash",
    num_questions: int = 5,
) -> str:
    """Generate questions based on the text via llm_service."""
    t = (text or "").strip()
    if not t: return "No content available to generate questions."

    prompt = (
        f"You will receive text from a document. Generate {num_questions} insightful questions "
        "based on the content to test the reader's understanding. "
        "Return only the questions as a plain text list using '-' for each item, instead of bullet points. "
        "Do not include markdown formatting like bolding unless helpful.\n\n"
        f"Text:\n{t}"
    )

    result, source = call_llm(prompt, api_key=api_key, model_name=model_name, temperature=0.5)
    if result:
        result = result.replace("•", "-").replace("*", "-")
        return result

    return "Failed to generate questions. Please check your API key or connection."
