# 🎧 AudioBook Generator

Transform any PDF, DOCX, or TXT document into a high-quality audiobook using AI-powered text enrichment and Microsoft Edge neural text-to-speech voices.

---

## ✨ Features

- **Standard Mode** — Single narrator rewrites your document into engaging audiobook prose
- **Dramatized Mode** *(Innovative Feature)* — AI detects characters, dialogue, and emotional tone per scene. Each character is assigned a unique neural voice with emotion-aware speaking rate and pitch — turning any document into a fully cast audio drama
- **Multi-language support** — English, Hindi, Tamil, Telugu, Bengali, Malayalam, Marathi, Kannada, Gujarati, and Urdu voices
- **Auto LLM switching** — Automatically selects the best available AI provider (Gemini → Groq → OpenAI) from your `.env` — no manual selection needed
- **No ffmpeg required** — Audio merging works without any system dependencies

---

## 🖥️ Demo

| Mode | What you get |
|------|-------------|
| Standard | Single narrator, clean audiobook narration |
| Dramatized | Multiple character voices, emotion-driven delivery |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/sampleaudio.git
cd sampleaudio
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- **Windows (PowerShell)**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (CMD)**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **macOS / Linux**
  ```bash
  source venv/bin/activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

Open `.env` and add your API keys:

```env
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
GROQ_API_KEY=your_groq_key_here
```

You only need **one** key to run the app. The app tries providers in this order:
**Gemini → Groq → OpenAI**

| Provider | Get your key |
|----------|-------------|
| Google Gemini (recommended — free tier available) | https://aistudio.google.com/app/apikey |
| Groq (free tier available) | https://console.groq.com/keys |
| OpenAI | https://platform.openai.com/api-keys |

### 5. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```
sampleaudio/
├── app.py                        # Main Streamlit application
├── requirements.txt              # Python dependencies
├── .env.example                  # API key template
├── modules/
│   ├── extractor.py              # Text extraction (PDF, DOCX, TXT)
│   ├── llm_auto.py               # Auto-switching LLM provider
│   ├── llm_enrichment.py         # Text enrichment & dramatization
│   ├── tts_converter.py          # Edge TTS voice conversion
│   └── audio_delivery.py         # Audio file handling
└── output/                       # Generated audiobooks saved here
```

---

## 🎙️ Available Voices

### English
| Voice | Gender | Accent |
|-------|--------|--------|
| Aria | Female | US |
| Jenny | Female | US |
| Guy | Male | US |
| Brian | Male | US |
| Emma | Female | US |
| Ryan | Male | UK |
| Sonia | Female | UK |
| William | Male | AU |
| Neerja | Female | Indian English |

### Indian Languages
| Language | Female | Male |
|----------|--------|------|
| Hindi | Swara | Madhur |
| Tamil | Pallavi | Valluvar |
| Telugu | Shruti | Mohan |
| Bengali | Tanishaa | Bashkar |
| Malayalam | Sobhana | Midhun |
| Marathi | Aarohi | Manohar |
| Kannada | Sapna | Gagan |
| Gujarati | Dhwani | Niranjan |
| Urdu | Gul | Salman |

---

## 🎬 How to Use

1. **Upload** a PDF, DOCX, or TXT file using the file uploader
2. **Select a narrator voice** from the sidebar (choose a voice matching your document's language)
3. **Choose a generation mode**:
   - *Standard* — best for articles, reports, non-fiction
   - *Dramatized* — best for stories, scripts, dialogue-heavy content
4. Click **Generate AudioBook**
5. **Listen** in the browser or **download** the `.mp3` file

### Tamil / Indian Language Documents

Upload a document in any Indian language, select the matching narrator voice (e.g. *Pallavi (Female, Tamil)*), and choose **Dramatized** mode. The AI will keep the text in the original language and assign native voices to each character automatically.

---

## 🧪 Sample PDFs

Two sample PDFs are included for testing:

| File | Language | Mode |
|------|----------|------|
| `sample_dramatized_story.pdf` | English | Dramatized |
| `sample_tamil_dramatized.pdf` | Tamil | Dramatized |

---

## ⚙️ Requirements

- Python 3.9+
- Internet connection (for LLM API calls and Edge TTS)
- At least one API key (Gemini, Groq, or OpenAI)

> **Note:** ffmpeg is optional. If not installed, audio segments are merged using raw binary concatenation, which works correctly for playback.

---

## 🛠️ Troubleshooting

| Error | Fix |
|-------|-----|
| `All LLM providers failed: no API key configured` | Make sure `.env` exists and contains at least one valid API key |
| `TTS conversion failed` | Check your internet connection (Edge TTS requires network access) |
| `Text extraction failed` | Ensure the PDF is not password-protected or image-only (scanned) |
| Gemini 404 model error | The app uses `gemini-2.0-flash` — ensure your key has access |

---

## 📄 License

MIT License — feel free to use, modify, and distribute.
