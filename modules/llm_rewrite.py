import os
from dotenv import load_dotenv
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")


# ---------- SPLIT TEXT ----------
def split_text(text, chunk_size=2500):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start = end

    return chunks


# ---------- REWRITE SINGLE CHUNK ----------
def rewrite_chunk(chunk, style):

    prompt = f"""
Convert the following text into a natural audiobook narration.

Narration style: {style}

Keep the meaning exactly the same.
Do NOT expand the content.

Text:
{chunk}
"""

    response = model.generate_content(prompt)

    if hasattr(response, "text") and response.text:
        return response.text

    if hasattr(response, "candidates"):
        return response.candidates[0].content.parts[0].text

    return chunk


# ---------- MAIN REWRITE FUNCTION ----------
def rewrite_text(text, style):

    try:

        chunks = split_text(text)

        rewritten_chunks = []

        with ThreadPoolExecutor(max_workers=4) as executor:

            results = executor.map(lambda c: rewrite_chunk(c, style), chunks)

        for r in results:
            rewritten_chunks.append(r)

        return "\n".join(rewritten_chunks)

    except Exception:
        return text