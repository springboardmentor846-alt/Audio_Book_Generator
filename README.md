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
git clone <your-repo-link>
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

---

## 📂 Project Structure

```text
Audio_Book_Generator
├── app.py
├── modules/
├── requirements.txt
├── avatar.jpg
├── README.md
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

## 🙌 Author

**Mohit**
B.Tech CSE | AI Developer | Infosys Springboard Intern
