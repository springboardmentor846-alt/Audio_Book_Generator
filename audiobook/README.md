# 🎧 AudioBook Generator

Convert your documents into engaging audiobooks with AI-powered text enhancement.

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up API key (optional, for LLM enhancement):**
```bash
# For OpenRouter (recommended - access to multiple models)
set OPENROUTER_API_KEY=your_key_here

# OR for OpenAI
set OPENAI_API_KEY=your_key_here

# OR for Google Gemini
set GEMINI_API_KEY=your_key_here
```

3. **Run the application:**
```bash
streamlit run app.py
```

4. **Open your browser** at `http://localhost:8501`

## Features

- 📄 Support for PDF, DOCX, and TXT files
- 🤖 Optional LLM enhancement for better narration
- 🎙️ Text-to-speech conversion
- ⬇️ Download generated audiobooks
- 🎵 In-browser audio preview

## Usage

1. Upload one or more documents
2. Configure settings in the sidebar
3. Click "Generate AudioBook"
4. Download or listen to your audiobook

## Technology Stack

- **Frontend:** Streamlit
- **Text Extraction:** PyPDF2, python-docx
- **LLM:** OpenAI GPT / Google Gemini
- **TTS:** pyttsx3

## Notes

- LLM enhancement requires an API key (OpenAI or Gemini)
- Without API key, the app works with original text
- Audio files are saved in the `output/` directory
