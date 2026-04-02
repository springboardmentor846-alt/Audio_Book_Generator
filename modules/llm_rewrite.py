import os
import re
from groq import Groq

# Split long text into chunks
def split_text(text, chunk_size=1000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def rewrite_for_audiobook(text):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    chunks = split_text(text)
    final_output = ""

    for chunk in chunks:
        prompt = f"""
Convert the following text into audiobook narration.

Rules:
1. Only return plain narration text
2. No extra instructions, no stage directions
3. No brackets [], no labels
4. Keep it natural and engaging

Text:
{chunk}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        result = response.choices[0].message.content

        # Clean unwanted bracket text (extra safety)
        result = re.sub(r"\[.*?\]", "", result)

        final_output += result + " "

    return final_output.strip()