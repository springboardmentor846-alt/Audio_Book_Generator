import streamlit as st
from modules.text_extraction import extract_text
from modules.llm_rewrite import rewrite_for_audiobook
from modules.tts import text_to_speech

st.set_page_config(page_title="AudioBook Generator", layout="wide")

# ---------- HEADER ----------
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>📘 AudioBook Generator</h1>
    <p style='text-align: center;'>Upload → Rewrite → Listen → Download</p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------- FILE UPLOAD ----------
st.subheader("📂 Upload Document")

uploaded_file = st.file_uploader(
    "Upload a document (PDF, DOCX, TXT, OR SCANNED PDF)",
    type=["pdf", "docx", "txt"]
)
if uploaded_file:
    st.success(f"File uploaded: {uploaded_file.name}")

    extracted_text = extract_text(uploaded_file)

    # ✅ Single check only
    if not extracted_text.strip():
        st.warning("⚠️ No readable text found in the document.")
        st.stop()

    

    # ---------- TEXT DISPLAY ----------
    st.subheader("📄 Extracted Text")
    st.text_area("", extracted_text, height=180)

    st.divider()

    # ---------- REWRITE ----------
    st.subheader("✍️ Generate Audiobook Text")

    if st.button("✨ Rewrite Text"):
        with st.spinner("Rewriting text..."):
            st.session_state.rewritten_text = rewrite_for_audiobook(extracted_text)

    # ---------- SHOW REWRITTEN TEXT ----------
    if "rewritten_text" in st.session_state:
        st.success("Text rewritten successfully!")

        st.text_area(
            "📘 Audiobook Narration",
            st.session_state.rewritten_text,
            height=180
        )

        st.divider()

        # ---------- AUDIO ----------
        st.subheader("🎧 Generate Audiobook Audio")

        # ✅ LIMIT TEXT FOR SPEED
        MAX_AUDIO_CHARS = 1500
        text_for_audio = st.session_state.rewritten_text[:MAX_AUDIO_CHARS]


        if st.button("🎙️ Generate Audio"):
            with st.spinner("Generating audiobook audio..."):
                audio_path = text_to_speech(text_for_audio)

            st.success("Audiobook generated successfully!")

            st.audio(audio_path, format="audio/mp3")

            with open(audio_path, "rb") as f:
                st.download_button(
                    "⬇️ Download Audiobook",
                    data=f,
                    file_name="audiobook.mp3",
                    mime="audio/mp3"
                )

# ---------- FOOTER ----------
st.divider()
st.markdown(
    "<p style='text-align: center; color: gray;'>Built using Streamlit • LLaMA • gTTS</p>",
    unsafe_allow_html=True
)