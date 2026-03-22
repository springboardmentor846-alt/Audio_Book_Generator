# import streamlit as st
# from extractor import extract_text
# from tts import text_to_speech
# from llm_processor import rewrite_text

# st.title("🎧 AI Audiobook Generator")

# uploaded_file = st.file_uploader("Upload file", type=["pdf", "docx", "txt"])

# if uploaded_file is not None:
#     text = extract_text(uploaded_file)

#     st.subheader("Extracted Text")
#     st.text_area("Text Output", text, height=200)

#     # 🔊 Voice Settings
#     st.subheader("Voice Settings")

#     language_dict = {
#         "English": "en",
#         "Hindi": "hi",
#         "Tamil": "ta",
#         "French": "fr"
#     }

#     selected_language = st.selectbox(
#         "Select Language",
#         list(language_dict.keys())
#     )

#     language = language_dict[selected_language]

#     speed_option = st.radio("Speech Speed", ["Normal", "Slow"])
#     slow = True if speed_option == "Slow" else False

#     if st.button("🎙 Generate AI Audiobook"):

#         with st.spinner("Enhancing text using AI..."):
#             rewritten_text = rewrite_text(text, selected_language)

#         with st.spinner("Generating audio..."):
#             audio_file = text_to_speech(
#                 rewritten_text,
#                 language=language,
#                 slow=slow
#             )

#         audio_bytes = open(audio_file, "rb").read()

#         st.success("Audiobook Generated Successfully 🎉")
#         st.audio(audio_bytes, format="audio/mp3")

#         st.download_button(
#             label="Download Audiobook",
#             data=audio_bytes,
#             file_name="audiobook.mp3",
#             mime="audio/mp3"
#         )
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from extractor import extract_text
from llm_processor import rewrite_text
from tts import text_to_speech
import os

app = Flask(__name__)

# Allow requests from React (http://localhost:3000)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = "uploads"
AUDIO_FILE = "audiobook.mp3"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/upload", methods=["POST", "OPTIONS"])
def upload_file():
    try:
        if request.method == "OPTIONS":
            # Handle preflight request
            return jsonify({"message": "CORS preflight OK"}), 200

        file = request.files.get("file")

        if not file:
            return jsonify({"error": "No file received"}), 400

        voice_gender = request.form.get("voice_gender", "Female")
        speed = request.form.get("speed", "Normal")

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        print("File received:", filepath)

        # 1️⃣ Extract text
        text = extract_text(filepath)
        
        if not text or not text.strip():
            return jsonify({"error": "No text could be extracted. Please ensure the file contains readable text."}), 400

        # 2️⃣ Rewrite text
        try:
            # We hardcode to English since language options were removed from UI
            rewritten_text = rewrite_text(text, "English")
        except Exception as e:
            print(f"Warning: rewrite_text failed: {e}. Falling back to original text.")
            rewritten_text = text

        # 3️⃣ Generate speech
        slow = True if speed == "Slow" else False

        audio_file = text_to_speech(
            rewritten_text,
            voice_gender=voice_gender,
            slow=slow,
            output_file="audiobook.mp3"
        )

        print("Audio generated:", audio_file)

        return jsonify({
            "message": "Audiobook generated successfully",
            "audio_url": "http://127.0.0.1:5000/audio",
            "extracted_text": rewritten_text
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/audio")
def get_audio():

    if not os.path.exists("audiobook.mp3"):
        return jsonify({"error": "Audio file not generated yet"}), 404

    return send_file("audiobook.mp3", mimetype="audio/mpeg")


if __name__ == "__main__":
    app.run(debug=True)