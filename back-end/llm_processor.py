from openai import OpenAI


client = OpenAI(api_key="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")


def rewrite_text(text, target_language="English"):
    if len(text) > 4000:
        text = text[:4000]

    prompt = f"""
    Rewrite and translate the following text into {target_language}.
    Make it suitable for audiobook narration with natural speaking tone.

    Text:
    {text}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert audiobook narrator and translator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        print("OpenAI Error:", e)
        return text