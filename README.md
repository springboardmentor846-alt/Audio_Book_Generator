🎧 AI Audiobook Generator

A full-stack web application that transforms documents into engaging, podcast-style audiobooks using Groq AI.

🚀 Features
📄 Upload PDF, DOCX, or TXT files
🎙️ Generate podcast-style audiobook scripts using Groq AI (LLaMA3)
🔊 Listen with browser-based Text-to-Speech (play, pause, speed, volume control)
📝 AI-generated structured summaries
💬 Ask questions about your content (Q&A)
🧩 Generate a 5-question quiz with scoring
🔖 Bookmark important sections
📊 Get evaluation insights (accuracy, difficulty, recommendations)
🛠️ Tech Stack
Backend: Python, Flask
AI: Groq API (LLaMA3-8B)
Frontend: HTML5, CSS3, JavaScript
UI Framework: Bootstrap 5.3
Icons: Bootstrap Icons
Fonts: Playfair Display, DM Sans
Text-to-Speech: Web Speech API
📂 Project Structure
audiobook_generator/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
⚙️ Setup & Installation
1. Install Dependencies
pip install -r requirements.txt
2. Get Groq API Key
Visit: https://console.groq.com
Create an account
Generate your API key
3. Run the Application
python app.py

Open your browser:

http://localhost:5000
▶️ Usage
Enter your Groq API key
Upload a PDF, DOCX, or TXT file
Select audiobook language
Click Generate Podcast Audiobook
Explore:
Audiobook
Summary
Q&A
Quiz
Bookmarks
Evaluation
🔐 Environment Variable (Optional)

Windows (CMD)

set GROQ_API_KEY=your_key_here

Windows (PowerShell)

$env:GROQ_API_KEY="your_key_here"

Mac / Linux

export GROQ_API_KEY="your_key_here"

Then run:

python app.py
📡 API Endpoints
Method	Route	Description
GET	/	Main UI
POST	/api/generate-audiobook	Generate audiobook script
POST	/api/summarize	Summarize content
POST	/api/generate-qa	Answer user questions
POST	/api/generate-quiz	Generate quiz questions
POST	/api/evaluate	Evaluate comprehension & difficulty
