# AI AudioBook Generator

A Streamlit app that turns documents into an audiobook-style narration:

- Upload **PDF / DOCX / TXT**
- Extract text (PDF text extraction with **OCR fallback**)
- Rewrite into a chosen narration style using **Google Gemini**
- Generate audio using **gTTS**
- Ask questions about the uploaded document (RAG via **ChromaDB** + **SentenceTransformers**)

## Features

- **Narration styles**: Storytelling / Educational / Podcast
- **Document Q&A**: retrieval-augmented answers from the uploaded content
- **Download audio** from the UI

## Requirements

- **Python** 3.10+ recommended
- **Tesseract OCR (Windows)** (needed for scanned/image PDFs)
- A **Google Gemini API key** (environment variable `GOOGLE_API_KEY`)

## Setup (Windows / PowerShell)

From the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install streamlit python-dotenv google-generativeai gTTS chromadb sentence-transformers pdfplumber pytesseract python-docx
```

### Install Tesseract OCR (for scanned PDFs)

1. Install Tesseract for Windows (e.g., from the official installer).
2. Ensure it’s installed at:
   - `C:\Program Files\Tesseract-OCR\tesseract.exe`

This app currently uses a hard-coded path in `modules/extract.py`:

- `pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"`

If you installed it elsewhere, update that line.

## Configure environment variables

Create a file named `.env` in the project root:

```env
GOOGLE_API_KEY=your_key_here
```

## Run the app

```powershell
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## How to use

1. Upload one or more documents.
2. Pick a narration style.
3. Click **Generate Audiobook** for a file.
4. Listen in the browser and download the audio.
5. Use the **Ask Questions** section to query the document.

## Supported file types

- **PDF**: text extraction, with OCR fallback if text is missing
- **DOCX**
- **TXT**

## Notes / troubleshooting

- **Gemini errors / blank output**: confirm `GOOGLE_API_KEY` is set and valid.
- **OCR not working**: confirm Tesseract is installed and the path in `modules/extract.py` matches your machine.
- **First run is slow**: `sentence-transformers` downloads a model on first use; subsequent runs are faster.

