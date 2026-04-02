# 📘 AudioBook Generator

An interactive web app built with **Streamlit** that converts documents into engaging audiobook narration using LLMs and Text-to-Speech.

---

## 🚀 Features

- 📂 Upload documents (PDF, DOCX, TXT, Scanned PDFs)
- 🔍 Extract text using:
  - PDF parsing
  - OCR (Tesseract for scanned files)
- ✍️ Rewrite content into natural audiobook narration using LLM
- 🎧 Convert text to audio (MP3)
- ⬇️ Download generated audiobook

---

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit  
- **LLM:** Groq (LLaMA 3.1)  
- **OCR:** Tesseract + pdf2image  
- **Text Extraction:** pdfplumber, python-docx  
- **Text-to-Speech:** gTTS  

---

## 📁 Project Structure

```
.
├── app.py                  # Main Streamlit app
├── modules/
│   ├── text_extraction.py  # Handles PDF, DOCX, TXT & OCR
│   ├── llm_rewrite.py      # Converts text into narration style
│   └── tts.py              # Converts text to speech
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/audiobook-generator.git
cd audiobook-generator
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Install External Tools

#### ✅ Tesseract OCR
- Download and install Tesseract
- Update path in `text_extraction.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

#### ✅ Poppler (for PDF to Image)
- Download Poppler
- Update path:

```python
POPPLER_PATH = r"C:\poppler\Library\bin"
```

---

### 4. Set Environment Variable

Set your **Groq API Key**:

```bash
export GROQ_API_KEY="your_api_key_here"   # Linux/Mac
set GROQ_API_KEY=your_api_key_here       # Windows
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📌 Usage

1. Upload a document (PDF/DOCX/TXT)
2. Extract text automatically
3. Click **"Rewrite Text"**
4. Generate audiobook narration
5. Click **"Generate Audio"**
6. Listen or download MP3 🎧

---

## ⚡ Notes

- Audio generation is limited to **1500 characters** for speed
- OCR is automatically triggered for scanned PDFs
- Preprocessing improves OCR accuracy (contrast, sharpening, scaling)

---

## 🧠 Future Improvements

- 🔊 Voice selection (male/female, accents)
- 🌍 Multi-language support
- 📚 Full-length audiobook generation (chunked audio)
- 🎵 Background music support
- ☁️ Deployment (Streamlit Cloud / AWS)

---

## 🤝 Contributing

Feel free to fork this repo and submit pull requests!

---

## 📄 License

This project is open-source and available under the MIT License.
