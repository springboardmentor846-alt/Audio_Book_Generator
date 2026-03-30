import streamlit as st
from modules.text_extractor import extract_text
from modules.llm_processor import rewrite_text_for_audiobook
from modules.tts_engine import text_to_speech
from modules.avatar_video import generate_avatar_video

st.title("AI Audiobook Generator")

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    st.info("📄 Extracting text...")
    text = extract_text(uploaded_file, uploaded_file.name)

    st.success("Text Extracted ✅")
    st.text_area("Extracted Text", text, height=300)

st.subheader("🎛 Voice Settings")

voice_gender = st.selectbox(
    "Select Voice",
    ["Female", "Male"]
)

speed = st.selectbox(
    "Narration Speed",
    ["Slow", "Normal", "Fast"]
)

tone = st.selectbox(
    "Narration Tone",
    ["Storytelling", "Formal", "Emotional"]
)    

if uploaded_file:

    if st.button("Rewrite with AI and Generate Audiobook 🎧"):

        status = st.status("Rewriting with AI...", expanded=True)
        with status: 
            new_text = rewrite_text_for_audiobook(text, tone) 
            status.update(label="✅ AI rewriting completed!", state="complete")

        st.text_area("Audiobook Style Text", new_text, height=300)

        status = st.status("Generating Audiobook 🎧...", expanded=True)
        with status: 
            audio_file = text_to_speech(new_text, voice_gender, speed)
            st.session_state.audio_file = audio_file   # STORE HERE
            status.update(label="🎧 Audiobook generated successfully!", state="complete")

        st.audio(audio_file) 

        with open(audio_file, "rb") as f:
            st.download_button(
                "Download Audiobook",
                f,
                file_name="audiobook.mp3"
            ) 

    # SECOND BUTTON
    if st.button("Generate Talking Avatar 🎬"):

        # ✅ Check if audio exists
        if "audio_file" not in st.session_state:
            st.error("⚠️ Please generate audiobook first!")
        else:
            status = st.status("Generating talking avatar...", expanded=True)
            with status:
                video_file = generate_avatar_video(st.session_state.audio_file)
                status.update(label="🎬 Avatar video ready!", state="complete")

            st.video(video_file)

            with open(video_file, "rb") as f:
                st.download_button(
                    "Download Video",
                    f,
                    file_name="avatar_video.mp4"
                )