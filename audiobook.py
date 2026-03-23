import os

import streamlit as st

from audio_tts import generate_audio_file, get_voice_for_settings
from text_extraction import extract_text_from_file, handle_file_upload
from text_processing import clean_text, convert_to_language, enhance_text_for_audio


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

generate_audio = st.sidebar.checkbox("Generate Audio (MP3)", value=True)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset All", help="Clear all extracted and processed text"):
    reset_session()
    st.rerun()
st.sidebar.markdown("---")


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
                    audio_path = generate_audio_file(st.session_state["final_text"], voice_name)

                    if audio_path and os.path.exists(audio_path):
                        st.session_state["audio_path"] = audio_path
                        st.success("✅ Audio generated!")

                        with open(audio_path, "rb") as audio_file:
                            st.audio(audio_file.read(), format="audio/mp3")

                        with open(audio_path, "rb") as f:
                            st.download_button(
                                label="Download Audiobook MP3",
                                data=f,
                                file_name=f"audiobook_{language.lower()}.mp3",
                                mime="audio/mp3"
                            )
                    else:
                        st.error("Failed to generate audio file.")

            elif st.session_state.get("audio_path") and os.path.exists(st.session_state["audio_path"]):
                st.info("📻 Previously generated audio:")
                with open(st.session_state["audio_path"], "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
                with open(st.session_state["audio_path"], "rb") as f:
                    st.download_button(
                        label="Download Audiobook MP3",
                        data=f,
                        file_name=f"audiobook_{language.lower()}.mp3",
                        mime="audio/mp3"
                    )
    elif not st.session_state["extracted_text"]:
        st.info("👆 Upload a document to begin. Text is extracted automatically.")