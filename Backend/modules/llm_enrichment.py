
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


def rewrite_chunk(text, style="Standard", doc_type="Article"):


    # ---------------- STYLE CONTROL ---------------- #

    style_instruction = ""

    if style == "Dramatic":
        style_instruction = """
Use expressive pacing and emotional narration.
Enhance dramatic moments slightly while keeping the meaning intact.
"""

    elif style == "Cinematic":
        style_instruction = """
Create immersive narration with atmospheric pacing.
Add natural pauses and vivid descriptive flow.
"""

    # ---------------- DOCUMENT TONE CONTROL ---------------- #

    tone_map = {
        "Story": "Use a vivid storytelling tone with emotional pacing.",
        "Research Paper": "Use a clear academic explanation tone suitable for listening.",
        "Technical Documentation": "Use an instructional tone explaining ideas step-by-step.",
        "Study Notes": "Use a teaching tone like a tutor explaining concepts clearly.",
        "Article": "Use an engaging and informative narration tone."
    }

    tone_instruction = tone_map.get(
        doc_type,
        "Use a clear and natural narration tone."
    )

    # ---------------- PROMPT ---------------- #

    prompt = f"""
You are a professional audiobook narrator.

Document Type: {doc_type}

{tone_instruction}

{style_instruction}

Rewrite the following text into a smooth and engaging audiobook narration.

Rules:
- Do NOT summarize.
- Do NOT remove important content.
- Keep the original meaning intact.
- Improve flow for listening.
- Add natural pauses where appropriate.
- Do NOT add headings.
- Do NOT add markdown symbols like ### or **.
- Do NOT add commentary or explanations.
- Output only clean narration text.

Text:
{text}
"""

    # ---------------- GEMINI CALL ---------------- #

    try:
        response = model.generate_content(prompt)

        if response.text:
            return response.text.strip() if response.text else text
        else:
            return text

    except Exception as e:
        print("Gemini rewrite error:", e)

        # fallback → return original text
        return text

#for study mode


def rewrite_chunk_study(text, doc_type):
    prompt = f"""
You are an expert educator and instructional designer.

Your job is to convert raw study material into a HIGH-QUALITY LEARNING MODULE.

========================
🎯 OBJECTIVE
========================
Transform the input into:
1. Clear explanation (easy to understand)
2. Conceptual understanding (not rote)
3. High-quality questions (for active recall)
4. A structured mind map

========================
📘 CONTENT RULES
========================
- Explain like a great teacher (simple but not oversimplified)
- Use short paragraphs and bullet points
- Include examples wherever possible
- If technical (like programming), include code-style explanations
- Avoid fluff, filler, or repetition
- Maintain logical flow

========================
🧠 QUESTION RULES (VERY IMPORTANT)
========================
- Generate EXACTLY 5 questions
- Questions must be:
  ✔ Conceptual (not definition-based only)
  ✔ Directly based on the given content
  ✔ Clearly worded and meaningful
  ✔ Useful for exams or real understanding
   ✔ Ensure questions test understanding, not memorization

- DO NOT generate vague or broken questions like:
  ❌ "What is Data?"
  ❌ "What is Moreover, data?"

- GOOD examples:
  ✔ "What type of scoping does C use?"
  ✔ "Why is static scoping important in programming?"

- Each question MUST have a correct, clear answer

========================
🌳 MIND MAP RULES
========================
- Extract key concepts only
- Keep it hierarchical
- Avoid too many nodes (keep it clean)
- Max depth: 2–3 levels

========================
📤 OUTPUT FORMAT (STRICT)
========================

===CONTENT===
<well-structured explanation>

===QA===
Q1: ...
A1: ...

Q2: ...
A2: ...

Q3: ...
A3: ...

Q4: ...
A4: ...

Q5: ...
A5: ...

===MINDMAP===
{{
  "name": "Main Topic",
  "children": [
    {{
      "name": "Concept 1",
      "children": [
        {{ "name": "Subconcept" }}
      ]
    }},
    {{
      "name": "Concept 2"
    }}
  ]
}}

========================
🚫 STRICTLY AVOID
========================
- Do NOT include anything outside the format
- Do NOT repeat the input text directly
- Do NOT generate irrelevant questions
- Do NOT generate malformed JSON
- Do NOT summarize.
- Do NOT remove important content.
- Keep the original meaning intact.
- Improve flow for listening.
- Add natural pauses where appropriate.
- Do NOT add headings.
- Do NOT add markdown symbols like ### or ** or *.
- Output only clean narration text.

========================
INPUT TEXT:
{text}
"""
    # ---------------- GEMINI CALL ---------------- #

    try:
        response = model.generate_content(prompt)

        if response.text:
            return response.text.strip() 
        else:
            return ""

    except Exception as e:
        print("Gemini study error:", e)

        
        return ""
