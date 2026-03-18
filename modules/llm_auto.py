import os
from dotenv import load_dotenv

load_dotenv()

# Priority order: (provider, env_var, model)
_PROVIDER_ORDER = [
    ("gemini", "GEMINI_API_KEY",  "gemini-2.0-flash"),
    ("groq",   "GROQ_API_KEY",    "llama-3.3-70b-versatile"),
    ("openai", "OPENAI_API_KEY",  "gpt-4o-mini"),
]


def call_llm_auto(prompt: str) -> str:
    errors = []

    for provider, env_var, model in _PROVIDER_ORDER:
        api_key = os.getenv(env_var, "").strip()
        if not api_key:
            errors.append(f"{provider}: no API key configured")
            continue

        try:
            return _dispatch(prompt, provider, api_key, model)
        except Exception as exc:
            errors.append(f"{provider} ({model}): {exc}")
            continue  # try next provider

    raise RuntimeError(
        "All LLM providers failed:\n" + "\n".join(errors)
    )


def get_active_provider() -> str:
    """Return the name of the first provider that has a key configured."""
    for provider, env_var, _ in _PROVIDER_ORDER:
        if os.getenv(env_var, "").strip():
            return provider
    return "none"

def _dispatch(prompt: str, provider: str, api_key: str, model: str) -> str:
    if provider == "gemini":
        return _call_gemini(prompt, api_key, model)
    elif provider == "openai":
        return _call_openai(prompt, api_key, model)
    elif provider == "groq":
        return _call_groq(prompt, api_key, model)
    raise ValueError(f"Unknown provider: {provider}")


def _call_gemini(prompt: str, api_key: str, model: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    response = genai.GenerativeModel(model).generate_content(prompt)
    return response.text


def _call_openai(prompt: str, api_key: str, model: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def _call_groq(prompt: str, api_key: str, model: str) -> str:
    from groq import Groq
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
