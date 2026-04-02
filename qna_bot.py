from __future__ import annotations

import re
from dataclasses import dataclass

from config import client
from text_processing import clean_text, split_text


@dataclass
class QnAResult:
    answer: str
    used_chunks: list[str]


def _normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9\u0900-\u097F\s]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _select_relevant_chunks(document_text: str, question: str, max_chunks: int = 6) -> list[str]:
    """
    Lightweight retrieval: split document into chunks and pick the ones with
    highest keyword overlap with the question.
    """
    doc_chunks = split_text(document_text, chunk_size=1800)
    if not doc_chunks:
        return []

    q = _normalize(question)
    q_terms = set(t for t in q.split(" ") if len(t) >= 3)
    if not q_terms:
        return doc_chunks[: max_chunks]

    scored: list[tuple[int, str]] = []
    for ch in doc_chunks:
        c = _normalize(ch)
        c_terms = set(t for t in c.split(" ") if len(t) >= 3)
        score = len(q_terms & c_terms)
        scored.append((score, ch))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = [ch for score, ch in scored[:max_chunks] if score > 0]
    return top if top else doc_chunks[: max_chunks]


def answer_question(document_text: str, question: str, *, tone: str = "Professional") -> QnAResult:
    """
    Answer a question grounded in the provided document text.
    Uses a small retrieval step to keep the prompt size reasonable.
    """
    document_text = clean_text(document_text or "")
    question = (question or "").strip()
    if not document_text or not question:
        return QnAResult(answer="", used_chunks=[])

    chunks = _select_relevant_chunks(document_text, question, max_chunks=6)
    context = "\n\n---\n\n".join(chunks)

    prompt = f"""
You are a helpful assistant answering questions strictly based on the provided document context.
If the answer is not present in the context, say: "I don't know from the provided document."

Answer style: {tone}
Rules:
- Be concise but complete.
- Use plain text (no markdown).
- Do not invent facts.

QUESTION:
{question}

DOCUMENT CONTEXT:
{context}
"""

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You answer questions grounded in provided context."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    answer = resp.choices[0].message.content
    answer = clean_text(answer)
    return QnAResult(answer=answer, used_chunks=chunks)

