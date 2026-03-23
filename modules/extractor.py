import streamlit as st
import pypdf
import docx

@st.cache_data
def extract_text_from_pdf(file):
    """
    Extract text from a PDF file.
    """
    pdf_reader = pypdf.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

@st.cache_data
def extract_text_from_docx(file):
    """
    Extract text from a DOCX file.
    """
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

@st.cache_data
def extract_text_from_txt(file):
    """
    Extract text from a TXT file.
    """
    # Try different encodings if utf-8 fails, but default to utf-8.
    return file.getvalue().decode("utf-8")
