import base64
import os
import shutil
import re

import streamlit as st

from audio_tts import generate_audio_file, get_voice_for_settings
from qna_bot import answer_question
from text_extraction import extract_text_from_file, handle_file_upload
from text_processing import clean_text, convert_to_language, enhance_text_for_audio

SAVED_DIR = "saved_audiobooks"
os.makedirs(SAVED_DIR, exist_ok=True)


def _safe_filename(name: str) -> str:
    """
    Convert user-provided name to a filesystem-safe filename (no extension).
    """
    name = (name or "").strip()
    name = re.sub(r"[^\w\- ]+", "", name)
    name = re.sub(r"\s+", "_", name).strip("_")
    return name or "My_Audiobook"



st.set_page_config(page_title="AI AudioBook Generator", layout="wide")

st.title("AI AudioBook Generator")
st.write("Upload your PDF/DOCX/TXT and generate audiobook.")


for key, default in [
    ("extracted_text", ""),
    ("enhanced_text", ""),
    ("final_text", ""),
    ("audio_path", None),
    ("last_uploaded_file_id", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def reset_session():
    """Reset all session state variables."""
    st.session_state["extracted_text"] = ""
    st.session_state["enhanced_text"] = ""
    st.session_state["final_text"] = ""
    st.session_state["audio_path"] = None
    st.session_state["last_uploaded_file_id"] = None


st.sidebar.title("Settings")

tone = st.sidebar.selectbox(
    "Narration Style",
    ["Professional", "Storytelling", "Motivational", "Podcast Style"],
)

language = st.sidebar.selectbox(
    "Audio Language",
    ["English", "Hindi", "Marathi"],
)

voice_gender = st.sidebar.selectbox(
    "Voice Gender",
    ["Female", "Male"],
)

enable_qna_audio = st.sidebar.checkbox("QnA answer as Audio", value=True)

speech_speed = st.sidebar.slider("Speech Speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
speed_percent = int((speech_speed - 1.0) * 100)
rate_str = f"+{speed_percent}%" if speed_percent >= 0 else f"{speed_percent}%"

generate_audio = st.sidebar.checkbox("Generate Audio (MP3)", value=True)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset All", help="Clear all extracted and processed text"):
    reset_session()
    st.rerun()
st.sidebar.markdown("---")


st.sidebar.markdown("---")

tab_generator, tab_saved, tab_qna = st.tabs(["🎙️ Generator", "📚 Saved Audiobooks", "❓ QnA Bot"])

with tab_generator:
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.subheader("Upload Document")
        uploaded_file = handle_file_upload()

        if uploaded_file:
            
            file_id = f"{uploaded_file.name}_{uploaded_file.size}"
            if st.session_state.get("last_uploaded_file_id") != file_id:
                with st.spinner("Extracting text from document..."):
                    extracted = extract_text_from_file(uploaded_file)
                    extracted = clean_text(extracted)
                    st.session_state["extracted_text"] = extracted
                    st.session_state["last_uploaded_file_id"] = file_id
                    st.session_state["enhanced_text"] = ""
                    st.session_state["final_text"] = ""
                    st.session_state["audio_path"] = None
                st.success("✅ File uploaded and text extracted automatically!")
            else:
                st.success("✅ File uploaded.")

            if st.session_state["extracted_text"]:
                st.subheader("Extracted Text Preview")
                st.text_area("Extracted Text", st.session_state["extracted_text"][:4000], height=250, key="extracted_preview")

                
                if st.button("Enhance Text for Audio (Groq AI)", type="primary"):
                    with st.spinner("Enhancing text and converting to selected language..."):
                        enhanced = enhance_text_for_audio(st.session_state["extracted_text"], tone)
                        st.session_state["enhanced_text"] = enhanced
                        final = convert_to_language(enhanced, language)
                        st.session_state["final_text"] = final
                    st.success("✅ Text enhanced and ready for audio!")

    with col2:
        st.subheader("Audiobook Output")

        if st.session_state["enhanced_text"]:
            st.text_area("Audio-Friendly Text", st.session_state["enhanced_text"][:3000], height=180, key="enhanced_preview")

        if st.session_state["final_text"]:
            st.text_area("Final Audiobook Text", st.session_state["final_text"], height=220, key="final_preview")

            if generate_audio:
                if st.button("Generate MP3 Audio (Edge TTS)", type="primary"):
                    with st.spinner("Generating natural-sounding audiobook voice..."):
                        voice_name = get_voice_for_settings(language, voice_gender)
                        audio_path = generate_audio_file(st.session_state["final_text"], voice_name, rate=rate_str)

                        if audio_path and os.path.exists(audio_path):
                            st.session_state["audio_path"] = audio_path
                            st.success("✅ Audio generated!")
                        else:
                            st.error("Failed to generate audio file.")

                if st.session_state.get("audio_path") and os.path.exists(st.session_state["audio_path"]):
                    st.info("📻 Currently Generated Audio:")
                    with open(st.session_state["audio_path"], "rb") as audio_file:
                        st.audio(audio_file.read(), format="audio/mp3")

                    with open(st.session_state["audio_path"], "rb") as f:
                        st.download_button(
                            label="Download Audiobook MP3",
                            data=f,
                            file_name=f"audiobook_{language.lower()}.mp3",
                            mime="audio/mp3"
                        )

                    st.markdown("---")
                    st.subheader("💾 Save to Library")
                    save_name = st.text_input("Name your audiobook", value="My_Audiobook")
                    if st.button("Save to Library"):
                        safe_name = _safe_filename(save_name)
                        dest_path = os.path.join(SAVED_DIR, f"{safe_name}.mp3")
                        shutil.copy(st.session_state["audio_path"], dest_path)
                        st.success(f"✅ Saved as '{safe_name}.mp3'!")
                        st.rerun()

        elif not st.session_state["extracted_text"]:
            st.info("👆 Upload a document to begin. Text is extracted automatically.")

with tab_saved:
    st.subheader("Your Saved Audiobooks")
    st.markdown("Saved files persist across refresh. You can rename or delete them anytime.")
    
    saved_files = sorted([f for f in os.listdir(SAVED_DIR) if f.lower().endswith(".mp3")])
    
    if not saved_files:
        st.info("No audiobooks saved yet. Generate and save one from the Generator tab.")
    else:
        for f_name in saved_files:
            file_path = os.path.join(SAVED_DIR, f_name)
            with st.expander(f"🎧 {f_name}"):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    with open(file_path, "rb") as audio_file:
                        b64 = base64.b64encode(audio_file.read()).decode()
                        
                    safe_id = "".join(c for c in f_name if c.isalnum())
                    
                    audio_html = f"""
                    <audio id="audio_{safe_id}" controls style="width: 100%;">
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                    <script>
                    (function() {{
                        const audio = document.getElementById("audio_{safe_id}");
                        const key = "audio_pos_{safe_id}";
                        const savedPos = localStorage.getItem(key);
                        
                        if (savedPos !== null) {{
                            audio.currentTime = parseFloat(savedPos);
                        }}
                        
                        audio.addEventListener("timeupdate", function() {{
                            localStorage.setItem(key, audio.currentTime);
                        }});
                    }})();
                    </script>
                    """
                    st.components.v1.html(audio_html, height=70)

                    new_name = st.text_input(
                        "Rename file (without .mp3)",
                        value=os.path.splitext(f_name)[0],
                        key=f"rename_{f_name}",
                    )
                    col_r, col_d = st.columns([1, 1])
                    with col_r:
                        if st.button("Rename", key=f"rename_btn_{f_name}"):
                            safe_new = _safe_filename(new_name)
                            new_path = os.path.join(SAVED_DIR, f"{safe_new}.mp3")
                            if new_path != file_path:
                                if os.path.exists(new_path):
                                    st.error("A file with that name already exists.")
                                else:
                                    os.rename(file_path, new_path)
                                    st.success("Renamed successfully.")
                                    st.rerun()
                    with col_d:
                        if st.button("Delete", key=f"delete_btn_{f_name}"):
                            os.remove(file_path)
                            st.success("Deleted.")
                            st.rerun()
                
                with col_b:
                    with open(file_path, "rb") as audio_f:
                        st.download_button(
                            "Download",
                            data=audio_f,
                            file_name=f_name,
                            mime="audio/mp3",
                            key=f"dl_{f_name}",
                        )

with tab_qna:
    st.subheader("QnA Bot (Ask questions about your document)")
    if not st.session_state.get("extracted_text"):
        st.info("Upload a document in the Generator tab first (text is extracted automatically).")
    else:
        question = st.text_input("Ask a question about the uploaded document", key="qna_question")
        if st.button("Get Answer", type="primary", disabled=not bool(question.strip()), key="qna_btn"):
            with st.spinner("Thinking..."):
                result = answer_question(st.session_state["extracted_text"], question, tone=tone)
                st.session_state["qna_answer"] = result.answer

        answer = st.session_state.get("qna_answer", "")
        if answer:
            st.text_area("Answer", answer, height=200, key="qna_answer_area")
            if enable_qna_audio:
                if st.button("Generate Answer Audio", key="qna_audio_btn"):
                    with st.spinner("Generating answer audio..."):
                        voice_name = get_voice_for_settings(language, voice_gender)
                        audio_path = generate_audio_file(answer, voice_name, rate=rate_str)
                        if audio_path and os.path.exists(audio_path):
                            st.audio(open(audio_path, "rb").read(), format="audio/mp3")
                            with open(audio_path, "rb") as f:
                                st.download_button(
                                    "Download Answer MP3",
                                    data=f,
                                    file_name="qna_answer.mp3",
                                    mime="audio/mp3",
                                )