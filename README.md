# 🎧 AI Audiobook & Study Assistant

An intelligent system that converts documents into audiobooks and interactive study material — built with a focus on **learning, retention, and usability**.

---

##  Overview
This project transforms static content (PDFs, notes, documents) into:

- 🎧 Immersive audiobooks (**Listener Mode**)
- 🎓 Structured learning modules (**Study Mode**)

It bridges the gap between passive consumption and active learning.

---

##  Core Features

### 🎧 Listener Mode
- Upload documents (PDF, text, etc.)
- Automatic text extraction & chunking
- AI-powered narration rewriting
- Multi-language audio generation
- Adjustable speed & volume controls
- Document-type-based narration tone

### 🎓 Study Mode (Advanced Learning)

#### 📘 Smart Notes Generation
- Converts raw content into structured explanations  
- Adds examples and conceptual clarity  
- Removes unnecessary fluff  

####  Mind Map Visualization
- Auto-generated hierarchical concept map  
- Interactive zoom & navigation (D3.js powered)  

####  Important Questions (LLM-based)
- 5 high-quality conceptual questions  
- Each includes:  
  - ✏️ Think (mental recall)  
  - 💡 Hint (guided clue)  
  - ✅ Answer (on-demand reveal)  

#### 🔊 Audio for Study Content
- Generate audio directly from study notes  
- Supports multiple languages  

---

##  Insights Dashboard

**Listener Insights**
- Total words  
- Audio duration  
- Content breakdown  
- Reading vs Listening comparison  

**Study Insights (Advanced)**
- Learning coverage  
- Concept density  
- Engagement metrics  
- Visual analytics & charts  

---

##  Tech Stack

**Frontend**
- React.js  
- Tailwind CSS  
- D3.js (Mind Maps)  
- Recharts (Analytics)  

**Backend**
- Flask (Python)  
- Gemini API (LLM)  
- PyTTSX3 (Offline TTS) 

---

## ⚙️ Architecture

Upload → Text Extraction → Chunking → LLM Processing
→ (Listener Mode OR Study Mode)

Listener Mode:
→ Rewrite → Audio → Insights

Study Mode:
→ Structured Notes → Q&A → Mind Map → Audio → Insights


---

## 🧩 Key Design Decisions
- ✅ Minimal LLM usage (cost-efficient)  
- ✅ LLM only used for:
  - Rewriting  
  - Mind map structure  
 

---

## 🧠 Study Mode Innovation
Instead of basic quizzes, this system focuses on:
- Active recall (Think → Hint → Answer)  
- Conceptual understanding  
- Structured learning  
- Visual learning (Mind Maps)  

---

## 📂 Project Structure




```
backend/
│
├── modules/
│   ├── extract_text.py
│   ├── text_chunker.py
│   ├── llm_enrichment.py
│   ├── cleaner.py
│   ├── text_to_speech.py
│   ├── parser.py
│   └── doc_detector.py
│
└── app.py

frontend/
│
├── pages/
│   ├── Upload.jsx
│   ├── StudyMode.jsx
│   ├── Insights.jsx
│   ├── StudyInsights.jsx
│   ├── Home.jsx
│
└── components/
    └── MindMap.jsx
```
```

---


## 🛠️ Setup Instructions

**Backend**
```bash
cd backend
pip install -r requirements.txt
python app.py
```
**Frontend**
```bash
cd frontend
npm install
npm run dev
```

**Environment Variables**
```bash
GEMINI_API_KEY=your_api_key_here
```
**Author**

Swati Singh
