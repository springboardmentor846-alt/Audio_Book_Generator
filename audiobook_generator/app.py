import os
import json
import re
from flask import Flask, request, jsonify, render_template
from groq import Groq
import PyPDF2
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def get_groq_client():

    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        return None, "GROQ_API_KEY not set. Run: export GROQ_API_KEY='your_key'"
    return Groq(api_key=api_key), None


def extract_text(file):
    filename = file.filename.lower()
    content = file.read()
    if filename.endswith('.pdf'):
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(content))
            return "\n".join(p.extract_text() for p in reader.pages).strip()
        except Exception:
            return None
    elif filename.endswith('.txt'):
        return content.decode('utf-8', errors='ignore')
    elif filename.endswith('.docx') or filename.endswith('.doc'):
        try:
            import zipfile
            from xml.etree import ElementTree as ET
            with zipfile.ZipFile(io.BytesIO(content)) as z:
                with z.open('word/document.xml') as doc:
                    root = ET.parse(doc).getroot()
                    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                    return ' '.join(t.text for t in root.findall('.//w:t', ns) if t.text)
        except Exception:
            return content.decode('utf-8', errors='ignore')
    return content.decode('utf-8', errors='ignore')


@app.route('/')
def index():
    api_configured = bool(os.environ.get('GROQ_API_KEY'))
    return render_template('index.html', api_configured=api_configured)


@app.route('/api/status')
def api_status():
    return jsonify({'configured': bool(os.environ.get('GROQ_API_KEY'))})


@app.route('/api/generate-audiobook', methods=['POST'])
def generate_audiobook():
    client, error = get_groq_client()
    if error:
        return jsonify({'error': error}), 401
    file = request.files.get('file')
    language = request.form.get('language', 'English')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400
    text = extract_text(file)
    if not text:
        return jsonify({'error': 'Could not extract text'}), 400
    text = text[:8000]
    prompt = f"""You are a professional audiobook narrator. Convert the following text into an engaging audiobook script in {language}. Provide ONLY the script.\n\nText:\n{text}"""
    try:
        c = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":prompt}], max_tokens=2000, temperature=0.7)
        return jsonify({'script': c.choices[0].message.content, 'original_text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/summarize', methods=['POST'])
def summarize():
    client, error = get_groq_client()
    if error:
        return jsonify({'error': error}), 401
    data = request.json
    text, language = data.get('text',''), data.get('language','English')
    if not text:
        return jsonify({'error': 'No text'}), 400
    prompt = f"Create a structured summary in {language} with: Executive Summary, Key Points, Conclusion.\n\nText:\n{text[:6000]}"
    try:
        c = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":prompt}], max_tokens=1500, temperature=0.5)
        return jsonify({'summary': c.choices[0].message.content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate-qa', methods=['POST'])
def generate_qa():
    client, error = get_groq_client()
    if error:
        return jsonify({'error': error}), 401
    data = request.json
    text, question, language = data.get('text',''), data.get('question',''), data.get('language','English')
    if not text or not question:
        return jsonify({'error': 'Text and question required'}), 400
    prompt = f"Answer this question in {language} based only on the text below: \"{question}\"\n\nText:\n{text[:5000]}"
    try:
        c = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":prompt}], max_tokens=800, temperature=0.4)
        return jsonify({'answer': c.choices[0].message.content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    client, error = get_groq_client()
    if error:
        return jsonify({'error': error}), 401
    data = request.json
    text, language = data.get('text',''), data.get('language','English')
    if not text:
        return jsonify({'error': 'No text'}), 400
    prompt = f"""Generate exactly 5 multiple-choice quiz questions in {language}. Return ONLY a valid JSON array, no markdown:\n[{{"question":"...","options":["A) ...","B) ...","C) ...","D) ..."],"correct":0,"explanation":"..."}}]\n\nText:\n{text[:5000]}"""
    try:
        c = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":prompt}], max_tokens=1500, temperature=0.4)
        raw = c.choices[0].message.content.strip()
        m = re.search(r'\[.*\]', raw, re.DOTALL)
        return jsonify({'quiz': json.loads(m.group() if m else raw)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    client, error = get_groq_client()
    if error:
        return jsonify({'error': error}), 401

    data = request.json
    original_text = data.get('original_text', '')
    script = data.get('script', '')
    language = data.get('language', 'English')

    if not original_text or not script:
        return jsonify({'error': 'Original text and script required'}), 400

    
    prompt = f"""
    You are an expert evaluator.

    Compare the ORIGINAL DOCUMENT and the GENERATED AUDIOBOOK SCRIPT.

    Evaluate ONLY these two metrics:

    1. accuracy_score (0-100): 
    How accurately the audiobook script preserves the meaning of the original document.

    2. comprehension_score (0-100): 
    How easy the audiobook is to understand when listened to.

    Return ONLY valid JSON:

    {{
    "accuracy_score": 0,
    "comprehension_score": 0
    }}

    ORIGINAL TEXT:
    {original_text[:3000]}

    AUDIOBOOK SCRIPT:
    {script[:3000]}
    """

    try:
        c = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=900,
            temperature=0.3
        )

        raw = c.choices[0].message.content.strip()

        # Extract JSON safely
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if not match:
            return jsonify({'error': 'Invalid response from model'}), 500

        evaluation = json.loads(match.group())

        return jsonify({'evaluation': evaluation})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not os.environ.get('GROQ_API_KEY'):
        print("\n" + "="*55)
        print("  WARNING: GROQ_API_KEY environment variable not set!")
        print("  Before running, execute in your terminal:")
        print("  export GROQ_API_KEY='gsk_your_key_here'")
        print("="*55 + "\n")
    else:
        print("\n  ✓ GROQ_API_KEY detected. Starting server...\n")
    app.run(debug=True, port=5000)
