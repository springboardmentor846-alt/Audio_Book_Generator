import os
import pdfplumber
from docx import Document


def extract_text(file_path):
    """
    Detect file type and route to appropriate extraction function.
    Supports: PDF, DOCX, TXT
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found.")

    file_extension = file_path.lower()

    if file_extension.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_extension.endswith(".docx"):
        return extract_text_from_docx(file_path)

    elif file_extension.endswith(".txt"):
        return extract_text_from_txt(file_path)

    else:
        raise ValueError(
            "Unsupported file format. Only PDF, DOCX, and TXT are supported."
        )


# ---------------- PDF Extraction ---------------- #

def extract_text_from_pdf(file_path):
    """
    Extract text from PDF while preserving basic structure.
    Note: Does not support scanned (image-based) PDFs.
    """

    text_blocks = []

    try:
        with pdfplumber.open(file_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()

                if page_text:
                    text_blocks.append(page_text.strip())

        full_text = "\n".join(text_blocks)

        if not full_text.strip():
            raise ValueError(
                "PDF contains no extractable text. It may be a scanned document."
            )

        return full_text

    except Exception as e:
        raise RuntimeError(f"Error extracting PDF: {e}")


# ---------------- DOCX Extraction ---------------- #

def extract_text_from_docx(file_path):
    """
    Extract text from DOCX while preserving paragraph breaks.
    """

    paragraphs = []

    try:
        doc = Document(file_path)

        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text.strip())

        full_text = "\n\n".join(paragraphs)

        if not full_text.strip():
            raise ValueError("DOCX file contains no readable text.")

        return full_text

    except Exception as e:
        raise RuntimeError(f"Error extracting DOCX: {e}")


# ---------------- TXT Extraction ---------------- #

def extract_text_from_txt(file_path):
    """
    Extract text from plain TXT file.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        if not text.strip():
            raise ValueError("TXT file is empty.")

        return text.strip()

    except Exception as e:
        raise RuntimeError(f"Error extracting TXT: {e}")
