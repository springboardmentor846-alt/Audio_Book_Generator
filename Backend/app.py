from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

from modules.upload import save_uploaded_file
from modules.extract_text import extract_text
from modules.text_chunker import chunk_text
from modules.llm_enrichment import rewrite_chunk
from modules.text_to_speech import text_to_speech
from modules.cleaner import clean_narration_text
from modules.translator import translate_text
from modules.doc_detector import detect_document_type
from modules.llm_enrichment import rewrite_chunk_study
from modules.parser import parse_study_output

app = Flask(__name__)

# ✅ Strong CORS fix
CORS(app, resources={r"/*": {"origins": "*"}})
@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        return '', 200

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


# ================= UPLOAD =================
@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        file_path = save_uploaded_file(file)
        text = extract_text(file_path)
        chunks = chunk_text(text)
        doc_type, confidence = detect_document_type(text)

        return jsonify({
            "text": text,
            "chunks": chunks,
            "doc_type": doc_type,
            "confidence": confidence
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= REWRITE =================
@app.route("/rewrite", methods=["POST"])
def rewrite():
    try:
        data = request.json

        rewritten_chunks = []
        for chunk in data["chunks"]:
            rewritten = rewrite_chunk(chunk, data["style"], data["doc_type"])
            rewritten = clean_narration_text(rewritten)
            rewritten_chunks.append(rewritten)

        return jsonify({
            "rewritten_text": "\n\n".join(rewritten_chunks)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/rewrite-study", methods=["POST"])
def rewrite_study():
    try:
        data = request.json

        raw_output = rewrite_chunk_study(data["text"], data.get("doc_type", "Notes"))

        parsed = parse_study_output(raw_output)
        parsed["notes"] = clean_narration_text(parsed["notes"])
        return jsonify(parsed)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# ================= AUDIO =================
@app.route("/generate-audio", methods=["POST"])
def generate_audio():
    try:
        data = request.json

        text = clean_narration_text(data["text"])

        if data["language"] != "en":
            text = translate_text(text, data["language"])

        file_path = text_to_speech(
            text,
            int(data["rate"]),
            float(data["volume"]),
            data["language"]
        )

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= INSIGHTS =================
@app.route("/insights", methods=["POST"])
def insights():
    data = request.json

    return jsonify({
        "total_words": len(data["text"].split()),
        "total_chunks": len(data["chunks"]),
        "estimated_minutes": round(len(data["text"].split()) / 160),
        "doc_type": data["doc_type"],
        "confidence": data["confidence"]
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)