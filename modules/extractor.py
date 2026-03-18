import os


def extract_text(file_path: str, file_type: str) -> str:
    file_type = file_type.lower().strip(".")
    extractors = {
        "pdf": extract_from_pdf,
        "docx": extract_from_docx,
        "txt": extract_from_txt,
    }
    if file_type not in extractors:
        raise ValueError(f"Unsupported file type: {file_type}. Supported: pdf, docx, txt")
    return extractors[file_type](file_path)


def extract_from_pdf(file_path: str) -> str:
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text.strip()
    except Exception:
        pass

    try:
        import PyPDF2
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")

    return text.strip()


def extract_from_docx(file_path: str) -> str:
    try:
        from docx import Document
        doc = Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from DOCX: {e}")


def extract_from_txt(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read TXT file: {e}")


def chunk_text(text: str, max_chars: int = 3500) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    chunks = []
    import re
    sentences = re.split(r"(?<=[.!?])\s+", text)

    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chars:
            current_chunk += (" " if current_chunk else "") + sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            if len(sentence) > max_chars:
                for i in range(0, len(sentence), max_chars):
                    chunks.append(sentence[i:i + max_chars])
                current_chunk = ""
            else:
                current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
