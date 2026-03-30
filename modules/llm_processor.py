from google import genai
import os
from dotenv import load_dotenv

# Load .env variables (optional but good practice)
load_dotenv()

# Create Gemini client (NEW SDK STYLE)
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def rewrite_text_for_audiobook(text, tone):

    prompt = f"""
Rewrite the following text in {tone.lower()} audiobook narration style.
Make it engaging and pleasant to listen with maximum 100 charactors total. Don't add any special symbols or notes etc.

Text:
{text}
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text