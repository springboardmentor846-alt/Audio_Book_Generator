from google import genai
import os
import time
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
)

def rewrite_text(text, language="English"):

    if not text.strip():
        return "No text to rewrite."

    prompt = f"""
    Rewrite the following text into an engaging audiobook narration style.

    STRICT INSTRUCTIONS:
    - Output MUST be ONLY in {language}
    - DO NOT include English if {language} is not English
    - DO NOT provide multiple versions
    - DO NOT explain anything
    - Only return the final narration text

    TEXT:
    {text}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        if hasattr(response, "text"):
            return response.text.strip()

        return "⚠️ No response from AI"

    except Exception:
        return "⚠️ AI service unavailable"