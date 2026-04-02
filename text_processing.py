import re

import streamlit as st

from config import client


def clean_text(text: str) -> str:
    """Clean and normalize text for processing."""
    if not text:
        return ""
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def remove_markdown(text: str) -> str:
    """Remove markdown formatting from text."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"#+", "", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    return text.strip()


def split_text(text: str, chunk_size: int = 5000):
    """Split text into chunks for processing."""
    chunks = []
    while len(text) > chunk_size:
        split_index = text.rfind(".", 0, chunk_size)
        if split_index == -1:
            split_index = text.rfind(" ", 0, chunk_size)
        if split_index == -1:
            split_index = chunk_size
        chunks.append(text[: split_index + 1])
        text = text[split_index + 1 :].strip()
    if text:
        chunks.append(text)
    return chunks


def enhance_text_for_audio(text: str, tone_style: str) -> str:
    """
    Enhance text to be audio-friendly using Groq AI.
    Makes text natural, engaging, and optimized for narration.
    """
    if not text:
        return ""

    if client is None:
        st.warning("⚠️ GROQ API client not configured; using unmodified text for audio narration.")
        return clean_text(text)

    chunks = split_text(text, chunk_size=2500)
    final_text = ""

    progress_bar = st.progress(0)
    total_chunks = len(chunks)

    for i, chunk in enumerate(chunks):
        prompt = f"""
You are an expert audiobook narrator.
Rewrite the following text into an audiobook narration style. Make sure of the grammar in the sentences and all the punctuations.
The listener should feel like they are listening to a professionally narrated audiobook.
Tone: {tone_style}

Rules:
- Make it engaging and natural for spoken narration.
- Remove headings, page numbers, footnotes, and formatting marks.
- Break long sentences into shorter, clearer sentences.
- Add smooth transitions between ideas.
- Keep the exact meaning and facts unchanged.
- Use natural pauses and flow.
- Output should be plain text (no markdown, no special characters).

Text to enhance:
{chunk}
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "You rewrite text into audiobook narration style. Make it natural and engaging for spoken word.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )

            rewritten = response.choices[0].message.content
            rewritten = remove_markdown(rewritten)
            rewritten = clean_text(rewritten)

            final_text += rewritten + "\n\n"

            progress_bar.progress((i + 1) / total_chunks)
        except Exception as e:  # noqa: BLE001
            st.error(f"Error enhancing chunk {i+1}: {str(e)}")
            final_text += clean_text(chunk) + "\n\n"

    progress_bar.empty()
    return final_text.strip()


def _detect_language_group(text: str) -> str:
    """
    Rough language group detection based on characters.
    Returns one of: 'English', 'Devanagari', 'Other'.
    """
    if not text:
        return "Other"
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return "Other"

    ascii_letters = sum(1 for c in letters if "a" <= c.lower() <= "z")
    devanagari_letters = sum(1 for c in letters if "\u0900" <= c <= "\u097F")

    total = len(letters)
    if total == 0:
        return "Other"

    if ascii_letters / total >= 0.6:
        return "English"
    if devanagari_letters / total >= 0.4:
        return "Devanagari"
    return "Other"


def convert_to_language(text: str, target_language: str) -> str:
    """
    Convert text to the selected audio language using Groq:
    - Supports English, Hindi, and Marathi as targets.
    - Source can be English, Hindi, Marathi, or mixed; Groq infers the exact source.
    - This enables:
        * English → Hindi / Marathi
        * Hindi  → English / Marathi
        * Marathi → English / Hindi
    """
    if not text:
        return text

    if client is None:
        if target_language == "English":
            return clean_text(text)

        st.warning(
            "⚠️ GROQ API client not configured; skipping translation and using the original text instead."
        )
        return clean_text(text)

    target_language = target_language or "English"

    # Detect broad source language family for better instructions (English vs Devanagari)
    source_group = _detect_language_group(text)
    if source_group == "English":
        source_desc = "English"
    elif source_group == "Devanagari":
        source_desc = "Hindi or Marathi (Devanagari script)"
    else:
        source_desc = "its original language (possibly mixed or unknown)"

    # If both detected and target are clearly English, skip translation
    if source_group == "English" and target_language == "English":
        return text

    language_map = {
        "English": "English",
        "Hindi": "Hindi (Devanagari script)",
        "Marathi": "Marathi (Devanagari script)",
    }

    target_lang_name = language_map.get(target_language, target_language)

    chunks = split_text(text, chunk_size=2000)
    translated_text = ""
    progress_bar = st.progress(0)
    total_chunks = len(chunks)

    for i, chunk in enumerate(chunks):
        prompt = f"""
You are an expert translator for audiobook narration.

The source text is primarily in {source_desc}.
Translate the following text to {target_lang_name}.

Rules:
- Maintain the audiobook narration style and tone.
- Keep it natural, fluent, and engaging as spoken language.
- Preserve all meaning and context accurately.
- Use the most appropriate vocabulary for {target_lang_name}.
- Output should be plain text (no markdown).

Text to translate:
{chunk}
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert translator specializing in audiobook narration. Translate text to {target_lang_name} while maintaining natural narration style and high fluency.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
            )

            translated = response.choices[0].message.content
            translated = remove_markdown(translated)
            translated = clean_text(translated)

            translated_text += translated + "\n\n"

            progress_bar.progress((i + 1) / total_chunks)
        except Exception as e:  # noqa: BLE001
            st.error(f"Error translating chunk {i+1}: {str(e)}")
            translated_text += clean_text(chunk) + "\n\n"

    progress_bar.empty()
    return translated_text.strip()

