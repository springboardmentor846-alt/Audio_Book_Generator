import re

def clean_narration_text(text):
    """
    Cleans LLM output:
    - Removes markdown
    - Converts bullet points (*) → numbered list
    - Removes unwanted formatting
    """

    # ---------------- REMOVE HEADINGS ----------------
    text = re.sub(r'^#+\s.*$', '', text, flags=re.MULTILINE)

    # ---------------- REMOVE BOLD/ITALIC ----------------
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)

    # ---------------- REMOVE SINGLE * BULLETS ----------------
    lines = text.split("\n")
    cleaned_lines = []

    bullet_count = 1

    for line in lines:
        stripped = line.strip()

        # Detect bullet (* or -)
        if stripped.startswith("* ") or stripped.startswith("- "):
            cleaned_lines.append(f"{bullet_count}. {stripped[2:].strip()}")
            bullet_count += 1
        else:
            cleaned_lines.append(line)
            # Reset numbering if paragraph breaks
            if stripped == "":
                bullet_count = 1

    text = "\n".join(cleaned_lines)

    # ---------------- REMOVE PARENTHESIS CONTENT ----------------
    text = re.sub(r'\(.*?\)', '', text)

    # ---------------- REMOVE LABEL LINES ----------------
    text = re.sub(
        r'^(Tone|Mood|Style|Narration):.*$', '', text, flags=re.MULTILINE
    )

    # ---------------- REMOVE EXTRA SPACES ----------------
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    return text.strip()