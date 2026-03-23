## Audiobook Generator (PDF/DOCX/TXT → MP3)

Streamlit app that extracts text from documents, optionally cleans/summarizes it using AI (Gemini or Groq), and generates an MP3 using `edge-tts` with a premium UI.

### Key Features
- **Smart Text Extraction**: Extracts text from PDF (`pypdf`, `pdfplumber`), DOCX (`python-docx`), and TXT files.
- **AI Text Cleaning & Summarization**: Uses Google Gemini or Groq (Llama 3) to fix OCR errors and format text, or summarize long documents into concise audio versions. The summarization engine dynamically scales slider limits and guarantees the summary word count is strictly less than the original document.
- **High-Quality Text-to-Speech**: Uses `edge-tts` to generate natural-sounding voiceovers with multiple accents (US, British, Indian, Hindi) and voice types (Male, Female, Child).
- **Interactive UI**: Features dynamic speaking avatars, an embedded audio player, and a premium dark/light mode experience.
- **Study Tools**:
  - **📝 Notes Generator**: Automatically creates bullet-point summary notes from your documents, generate audio for notes and download audio button.
  - **❓ Questions Generator**: Uses AI to generate insightful questions to test your understanding, generate audio for questions and download audio button.
  - **📊 Audio Statistics**: View word counts and precise audio duration calculations (via `pydub`).

### Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your API keys:
   - Copy `.env.example` to `.env`
   - Set `GEMINI_API_KEY=...` (for Gemini models)
   - Set `GROQ_API_KEY=...` (Optional, for locally-configured Groq Llama models)

### Run

```bash
venv\Scripts\activate.bat  # (if using Windows command prompt)
streamlit run app.py
```

### Notes

- **Summarized audiobook** mode works even without API keys (it falls back to an extractive local summarizer), but Gemini/Groq usually gives better results.
- Long text is **chunked automatically** for `edge-tts` to handle large documents seamlessly without API limits.

---

## Technical Overview

This project is a complete web application that translates document files into an interactive audiobook experience.

### Core Components & Libraries

**1. Frontend & Application Logic**
*   **Files:** `app.py`, `next_app.py`, `ui_1.py`, `ui_2.py`
*   **Library:** `streamlit`
*   **Purpose:** Creates a beautiful, responsive web interface tailored with custom CSS gradients and dark/light modes. Includes dynamic multi-column layouts and animated speaker avatars.

**2. Document Processing**
*   **File:** `text_extraction.py`
*   **Libraries:** `pypdf`, `pdfplumber`, `python-docx`
*   **Purpose:** Standardizes text extraction across different static document formats. 

**3. AI Services (The "Brain")**
*   **Files:** `llm_service.py`, `gemini_helper.py`
*   **Libraries:** `google-genai`, `groq`
*   **Purpose:** Provides intelligent text cleaning, summarization, and question generation. Utilizes a graceful fallback waterfall strategy: tries the latest Gemini SDK, then older SDKs, then Groq, and finally basic regex parsing.

**4. Text-to-Speech Engine**
*   **File:** `tts.py`
*   **Libraries:** `edge-tts`, `pydub`
*   **Purpose:** Converts the text payload to speech chunks and merges them cleanly using `pydub`. Exposes a distinct variety of voice personalities mapping to specific regional endpoints.

**5. Configuration & Environment**
*   **File:** `.env`
*   **Library:** `python-dotenv`
*   **Purpose:** Securely manages required API keys for generative features.
