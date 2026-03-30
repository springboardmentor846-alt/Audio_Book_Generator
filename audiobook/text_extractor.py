import io
from pathlib import Path

def extract_text(uploaded_file):
    """Extract text from uploaded file based on type"""
    file_extension = Path(uploaded_file.name).suffix.lower()
    
    if file_extension == ".txt":
        return uploaded_file.read().decode("utf-8")
    
    elif file_extension == ".pdf":
        try:
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except ImportError:
            raise ImportError("PyPDF2 not installed. Run: pip install PyPDF2")
    
    elif file_extension == ".docx":
        try:
            from docx import Document
            doc = Document(io.BytesIO(uploaded_file.read()))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except ImportError:
            raise ImportError("python-docx not installed. Run: pip install python-docx")
    
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")
