import streamlit as st
from extractor import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
from llm import rewrite_with_llm
from tts import generate_audio

st.set_page_config(page_title="AI AudioBook Generator", layout="wide")

st.title("🎧 AI AudioBook Generator")
st.markdown("Upload a document and convert it into a professional AI-generated audiobook.")

uploaded_file = st.file_uploader(
    "Upload PDF, DOCX, or TXT",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    with st.spinner("Extracting text..."):
        file_type = uploaded_file.name.split(".")[-1].lower()

        if file_type == "pdf":
            extracted_text = extract_text_from_pdf(uploaded_file)
        elif file_type == "docx":
            extracted_text = extract_text_from_docx(uploaded_file)
        else:
            extracted_text = extract_text_from_txt(uploaded_file)

    if extracted_text.strip():
        st.success("Text extracted successfully!")

        voice_choice = st.selectbox(
            "Select Voice",
            ["female", "male"]
        )
        
        style_choice = st.selectbox(
            "Select Narration Style",
            ["short", "medium", "detailed"]
    )

        if st.button("🎧 Generate Audiobook"):
            try:
                with st.spinner("Rewriting with Gemini AI..."):
                    rewritten_text = rewrite_with_llm(extracted_text)

                st.subheader("✨ Audiobook Style Preview")
                st.text_area("Rewritten Content", rewritten_text, height=250)

                with st.spinner("Generating Neural Voice..."):
                    audio_file = generate_audio(rewritten_text, voice_choice)

                with open(audio_file, "rb") as f:
                    audio_bytes = f.read()

                st.subheader("🔊 Audio Output")
                st.audio(audio_bytes, format="audio/mp3")

                st.download_button(
                    label="⬇ Download Audiobook",
                    data=audio_bytes,
                    file_name="audiobook.mp3",
                    mime="audio/mp3"
                )

                st.success("Audiobook generated successfully!")

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("No readable text found in file.")