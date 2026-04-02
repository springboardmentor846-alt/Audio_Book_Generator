import streamlit as st
from modules.text_extractor import extract_text
from modules.llm_processor import rewrite_text_for_audiobook
from modules.tts_engine import text_to_speech
from modules.avatar_video import generate_avatar_video

# -------------------- HEADER --------------------
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🎧 AI Audiobook Generator</h1>",
    unsafe_allow_html=True
)

st.divider()

# -------------------- TOP LAYOUT --------------------
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "📂 Upload Document",
        type=["pdf", "docx", "txt"]
    )

with col2:
    st.markdown("### 📘 Instructions")
    st.write("""
    1. Upload your document  
    2. Choose voice settings  
    3. Generate audiobook 🎧  
    4. Create talking avatar 🎬  
    """)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.header("⚙ Voice Settings")

    voice_gender = "Female"

    speed = st.selectbox(
        "Narration Speed",
        ["Slow", "Normal", "Fast"]
    )

    tone = st.selectbox(
        "Narration Tone",
        ["Storytelling", "Formal", "Emotional"]
    )

# -------------------- TEXT EXTRACTION --------------------
text = None

if uploaded_file:
    try:
        st.info("📄 Extracting text...")
        text = extract_text(uploaded_file, uploaded_file.name)

        if not text or len(text.strip()) == 0:
            st.error("❌ No text extracted.")
            st.stop()

        st.success("✅ Text Extracted")

        with st.expander("📄 View Extracted Text"):
            st.text_area("", text, height=300)

    except Exception as e:
        st.error("🚨 Extraction Error")
        st.code(str(e))
        st.stop()
else:
    st.warning("⚠ Please upload a file first.")
    st.stop()

st.divider()

# -------------------- BUTTONS --------------------
col1, col2 = st.columns(2)

with col1:
    generate_audio = st.button("🎧 Generate Audiobook")

with col2:
    generate_video = st.button("🎬 Generate Avatar")

# -------------------- AUDIO GENERATION --------------------
if generate_audio:
    try:
        progress = st.progress(0)

        progress.progress(20)
        new_text = rewrite_text_for_audiobook(text, tone)

        if not new_text:
            st.error("❌ AI rewrite failed.")
            st.stop()

        with st.expander("🤖 View AI Text"):
            st.text_area("", new_text, height=300)

        progress.progress(60)
        audio_file = text_to_speech(new_text, voice_gender, speed)

        if not audio_file:
            st.error("❌ Audio generation failed.")
            st.stop()

        # ✅ STORE AUDIO
        st.session_state.audio_file = audio_file

        progress.progress(100)
        st.success("🎉 Audiobook ready!")

    except Exception as e:
        st.error("🚨 Audio Error")
        st.code(str(e))

# -------------------- VIDEO GENERATION --------------------
if generate_video:
    try:
        if "audio_file" not in st.session_state:
            st.error("⚠ Generate audiobook first!")
            st.stop()

        st.image("avatar.jpg", caption="🎭 Avatar Preview", width=200)

        video_file = generate_avatar_video(st.session_state.audio_file)

        if not video_file:
            st.error("❌ Video generation failed.")
            st.stop()

        # ✅ STORE VIDEO
        st.session_state.video_file = video_file

        st.success("🎬 Avatar ready!")

    except Exception as e:
        st.error("🚨 Video Error")
        st.code(str(e))

# -------------------- DISPLAY AUDIO --------------------
if "audio_file" in st.session_state:
    st.subheader("🎧 Your Audiobook")

    st.audio(st.session_state.audio_file)

    with open(st.session_state.audio_file, "rb") as f:
        st.download_button(
            "⬇ Download Audio",
            f,
            file_name="audiobook.mp3"
        )

# -------------------- DISPLAY VIDEO --------------------
if "video_file" in st.session_state:
    st.subheader("🎬 Your Avatar Video")

    st.video(st.session_state.video_file)

    with open(st.session_state.video_file, "rb") as f:
        st.download_button(
            "⬇ Download Video",
            f,
            file_name="avatar_video.mp4"
        )