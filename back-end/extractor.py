from PyPDF2 import PdfReader
from docx import Document
import os


def clean_text(text):
    lines = text.splitlines()
    cleaned = [line.strip() for line in lines if line.strip() != ""]
    return "\n".join(cleaned)


def extract_text(file_path):

    file_name = file_path.lower()
    text = ""

    if file_name.endswith(".pdf"):

        pdf = PdfReader(file_path)

        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    elif file_name.endswith(".docx"):

        doc = Document(file_path)

        for para in doc.paragraphs:
            text += para.text + "\n"

    elif file_name.endswith(".txt"):

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    else:
        return "Unsupported file format"

    return clean_text(text)