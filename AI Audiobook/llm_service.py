from __future__ import annotations
import os
from typing import Optional

def _import_gemini():
    """Try to import either google-genai or google-generativeai SDK."""
    try:
        from google import genai
        return genai
    except Exception:
        pass
    try:
        import google.generativeai as genai
        return genai
    except Exception:
        return None

def _import_groq():
    """Safely import the Groq client if available."""
    try:
        import groq
        return groq
    except Exception:
        return None

def is_gemini_available() -> bool:
    """Return True if a Gemini-capable SDK is installed."""
    return _import_gemini() is not None

def call_llm(
    prompt: str,
    api_key: Optional[str] = None,
    model_name: str = "gemini-2.0-flash",
    temperature: float = 0.2
) -> tuple[str, str]:
    """
    Core LLM call chain: Gemini (new SDK) -> Gemini (old SDK) -> Groq (Llama) -> Groq (backup).
    Returns (response_text, provider_name). Returns ("", "failed") if all fail.
    """
    gemini_key = (api_key or os.getenv("GEMINI_API_KEY", "")).strip()
    groq_llama_key = os.getenv("GROQ_llama", "").strip()
    groq_key = os.getenv("GROQ_API_KEY", "").strip()

    genai_module = _import_gemini() if gemini_key else None
    groq_module = _import_groq()

    # 1. Gemini (New SDK)
    if genai_module and hasattr(genai_module, "Client"):
        try:
            client = genai_module.Client(api_key=gemini_key)
            resp = client.models.generate_content(model=model_name, contents=prompt)
            text = (getattr(resp, "text", "") or "").strip()
            if text: return text, "gemini"
        except Exception:
            pass

    # 2. Gemini (Older SDK)
    if genai_module and hasattr(genai_module, "GenerativeModel"):
        try:
            genai_module.configure(api_key=gemini_key)
            model = genai_module.GenerativeModel(model_name)
            resp = model.generate_content(prompt)
            text = (getattr(resp, "text", "") or "").strip()
            if text: return text, "gemini"
        except Exception:
            pass

    # 3. Groq (Llama key)
    if groq_module and groq_llama_key:
        try:
            client = groq_module.Groq(api_key=groq_llama_key)
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            text = (resp.choices[0].message.content or "").strip()
            if text: return text, "groq"
        except Exception:
            pass

    # 4. Groq (Default key)
    if groq_module and groq_key:
        try:
            client = groq_module.Groq(api_key=groq_key)
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            text = (resp.choices[0].message.content or "").strip()
            if text: return text, "groq"
        except Exception:
            pass

    return "", "failed"
