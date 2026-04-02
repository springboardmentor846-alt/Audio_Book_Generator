import pdfplumber
from docx import Document
import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
from pdf2image import convert_from_bytes
import io
import streamlit as st

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Poppler path
POPPLER_PATH = r"C:\poppler\Library\bin"


def preprocess_image(img):
    """Enhance image quality for better OCR accuracy."""
    # Upscale image (higher DPI = better OCR)
    width, height = img.size
    img = img.resize((width * 2, height * 2), Image.LANCZOS)

    # Convert to grayscale
    img = img.convert("L")

    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)

    # Sharpen
    img = img.filter(ImageFilter.SHARPEN)

    return img


def extract_text(file):
    file_type = file.name.split('.')[-1].lower()

    # ---------- PDF ----------
    if file_type == "pdf":
        text = ""

        # Step 1: Try normal text extraction
        try:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            st.error(f"pdfplumber failed: {e}")

        # Step 2: If no text → use OCR with preprocessing
        if not text.strip():
            st.info("No direct text found. Trying OCR with image enhancement...")
            try:
                file.seek(0)
                images = convert_from_bytes(
                    file.read(),
                    dpi=300,               # Higher DPI for better quality
                    poppler_path=POPPLER_PATH
                )
                st.info(f"OCR: {len(images)} page(s) found. Extracting...")

                for i, img in enumerate(images):
                    # Preprocess image
                    processed = preprocess_image(img)

                    # Try multiple Tesseract configs
                    ocr_text = pytesseract.image_to_string(
                        processed,
                        config="--psm 6 --oem 3"  # psm 6 = assume uniform block of text
                    )

                    st.info(f"Page {i+1} OCR result (first 100 chars): {ocr_text[:100]}")
                    text += ocr_text + "\n"

            except Exception as e:
                st.error(f"OCR failed: {e}")

        return text.strip()

    # ---------- DOCX ----------
    elif file_type == "docx":
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    # ---------- TXT ----------
    elif file_type == "txt":
        return file.read().decode("utf-8")

    else:
        return ""