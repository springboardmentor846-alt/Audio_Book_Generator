import requests

API_KEY = "your_key"

def split_text(text, chunk_size=12000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def rewrite_chunk(chunk):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"Rewrite the following text in an engaging audiobook narration style:\n\n{chunk}"
                    }
                ]
            }
        ]
    }

    response = requests.post(url, json=data)
    result = response.json()

    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        raise Exception(result)

def rewrite_with_llm(text):
    chunks = split_text(text)
    rewritten = []

    for chunk in chunks:
        rewritten.append(rewrite_chunk(chunk))

    return "\n".join(rewritten)