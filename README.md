# 🎧 AI Audiobook Generator with Talking Avatar

An AI-powered application that transforms text into expressive audiobooks and generates a realistic talking avatar video.

---

## 🚀 Features

* ✨ **AI-powered text rewriting** for natural narration
* 🎙️ **Text-to-Speech (TTS)** audiobook generation
* 🎭 **Talking AI Avatar** using SadTalker
* 🎚️ **Narration Style Control** (custom tone & expression)
* 📄 Supports **PDF, DOCX, and Text input**
* 📥 Download:

  * Audiobook (MP3)
  * Avatar video (MP4)

---

## 🧠 How It Works

```text
User Input → AI Rewrite → Audio Generation → Avatar Video
```

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** (UI)
* **LLM-based text processing**
* **Text-to-Speech engine**
* **SadTalker (AI Avatar Generation)**

---

## ⚙️ Setup Instructions

### 🔹 1. Clone the Repository

```bash
git clone <https://github.com/springboardmentor846-alt/Audio_Book_Generator/edit/Mohit>
cd Audio_Book_Generator
```

---

### 🔹 2. Setup Main Environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ⚠️ SadTalker Setup (Important)

This project uses **SadTalker** for avatar generation, which requires a separate setup.

### 🔹 Step 1 — Use Python 3.10

SadTalker works best with Python 3.10.

### 🔹 Step 2 — Create Environment

```bash
py -3.10 -m venv sadtalker_env
sadtalker_env\Scripts\activate
```

### 🔹 Step 3 — Clone SadTalker

```bash
git clone https://github.com/OpenTalker/SadTalker.git
cd SadTalker
pip install -r requirements.txt
```

### 🔹 Step 4 — Download Required Models

Download and place inside:

```text
SadTalker/checkpoints/
```

Required files:

* SadTalker_V0.0.2_512.safetensors
* epoch_20.pth
* BFM_Fitting (folder)

---

## ▶️ Run the Application

```bash
streamlit run app.py
```
⏱ SadTalker Performance
| System Type        | Approx Time |
| ------------------ | ----------- |
| 💻 4GB RAM (i3)    | 25–40 min   |
| 💻 8GB RAM (i5)    | 10–25 min   |
| 💻 16GB RAM (i7)   | 5–12 min    |
| 🚀 GPU (Colab/RTX) | 1–3 min     |

---

## 📂 Project Structure

```text
audiobook-generator/
│
├── app.py
├── modules/
│   ├── text_extractor.py
│   ├── llm_processor.py
│   ├── tts_engine.py
│   ├── avatar_video.py
│
├── SadTalker/
│   ├── checkpoints/
│   ├── results/
│
├── avatar.jpg
├── requirements.txt
```

---

## 📌 Notes

* SadTalker setup is required **before using avatar feature**
* Separate environments are used for compatibility:

  * Python 3.13 → Main app
  * Python 3.10 → SadTalker

---

## 🌟 Highlights

* Real-world AI pipeline integration
* Multi-environment handling
* End-to-end system: Text → Audio → Video

---

## 🚨 Known Limitations
* Slow video generation on CPU
* gTTS lacks real voice variety
* Requires refresh for long-running tasks

## 🚀 Future Improvements
* Real human voices (Edge TTS)
* Faster GPU-based inference
* Auto-refresh UI for video completion
* Multiple avatar support
* Cloud deployment

## 🙌 Author

**Mohit**
B.Tech CSE | AI Developer | Infosys Springboard Intern
