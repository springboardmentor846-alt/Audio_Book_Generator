import streamlit as st

def upload_file():
    """
    Handles single or multiple document uploads.
    Supported formats: PDF, DOCX, TXT
    """
    return st.file_uploader(
        "Upload one or more documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )
