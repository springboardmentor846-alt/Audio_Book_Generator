import streamlit as st
import pdfplumber
import docx


def handle_file_upload():
    """Handle file upload and return the uploaded file object."""
    return st.file_uploader("Upload PDF / DOCX / TXT", type=["pdf", "docx", "txt"])


def extract_text_from_pdf(file):
    """Extract text from PDF file."""
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        st.error(f"Error extracting PDF: {str(e)}")
        return ""
    return text


def extract_text_from_docx(file):
    """Extract text from DOCX file."""
    text = ""
    try:
        doc_file = docx.Document(file)
        for para in doc_file.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        st.error(f"Error extracting DOCX: {str(e)}")
        return ""
    return text


def extract_text_from_txt(file):
    """Extract text from TXT file."""
    try:
        file.seek(0)
        content = file.read()
        if isinstance(content, bytes):
            text = content.decode("utf-8")
        else:
            text = content
        return text
    except Exception as e:
        st.error(f"Error extracting TXT: {str(e)}")
        return ""


def extract_text_from_file(uploaded_file):
    """
    Unified function to extract text from uploaded file.
    Supports PDF, DOCX, and TXT formats.
    """
    if not uploaded_file:
        return ""

    file_extension = uploaded_file.name.lower().split(".")[-1]

    if file_extension == "pdf":
        return extract_text_from_pdf(uploaded_file)
    if file_extension == "docx":
        return extract_text_from_docx(uploaded_file)
    if file_extension == "txt":
        return extract_text_from_txt(uploaded_file)

    st.error(f"Unsupported file format: {file_extension}")
    return ""

