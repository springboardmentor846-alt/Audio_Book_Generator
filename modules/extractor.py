import PyPDF2
import pdfplumber
from docx import Document

def extract_text(file):
    if file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        return "Unsupported file format"
