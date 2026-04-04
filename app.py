import streamlit as st
from modules.extractor import extract_text
from modules.llm_rewriter import rewrite_text
from modules.tts_converter import text_to_speech

# ✅ Page config
st.set_page_config(
    page_title="AI Audiobook Generator",
    page_icon="🎧",
    layout="centered"
)

# ✅ Header
st.title("🎧 AI Audiobook Generator")
st.markdown("Convert documents into natural-sounding audiobooks using AI.")

# =========================
# 🌍 LANGUAGE SETTINGS (FIXED POSITION)
# =========================
st.sidebar.header("🌍 Language Settings")

language = st.sidebar.selectbox(
    "Select Output Language",
    ["English", "Malayalam", "Hindi"]
)

# ✅ Language mapping
lang_map = {
    "English": "en",
    "Malayalam": "ml",
    "Hindi": "hi"
}

tts_lang = lang_map[language]

# =========================
# 📄 FILE UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "📄 Upload PDF, DOCX, or TXT file",
    type=["pdf", "docx", "txt"]
)

if uploaded_file is not None:

    st.success("✅ File uploaded successfully!")

    if st.button("🚀 Generate Audiobook"):

        # 🔹 Step 1: Extract
        with st.spinner("Extracting text..."):
            raw_text = extract_text(uploaded_file)

        # 🔹 Preview
        with st.expander("📄 View Extracted Text"):
            st.text_area("Original Text", raw_text[:1500], height=200)

        # 🔹 Step 2: Rewrite (PASS LANGUAGE)
        with st.spinner("Rewriting in audiobook style..."):
            rewritten_text = rewrite_text(raw_text[:4000], language)

        # 🔹 Show rewritten text
        with st.expander("🎙 View Audiobook Text"):
            st.text_area("Rewritten Text", rewritten_text, height=300)

        # 🔹 Step 3: Convert to audio (PASS TTS LANG)
        with st.spinner("Generating audio..."):
            audio_file = text_to_speech(rewritten_text, lang=tts_lang)

        if audio_file:

            st.subheader("🔊 Audiobook Audio")

            audio_bytes = open(audio_file, "rb").read()

            col1, col2 = st.columns([3, 1])

            with col1:
                st.audio(audio_bytes, format="audio/mp3")

            with col2:
                st.download_button(
                    label="⬇ Download",
                    data=audio_bytes,
                    file_name="audiobook.mp3",
                    mime="audio/mp3"
                )

            st.success("🎉 Audiobook generated successfully!")