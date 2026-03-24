from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
)

def rewrite_text(text):

    if not text.strip():
        return "No text to rewrite."

    prompt = f"""
    Rewrite the following text in engaging audiobook narration style.
    Make it expressive and natural.
    Keep the meaning same.

    TEXT:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text