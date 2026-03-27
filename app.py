import streamlit as st
from modules.upload import upload_file
from modules.extract import extract_text
from modules.llm_rewrite import rewrite_text
from modules.tts import text_to_speech
from modules.audio_delivery import deliver_audio
from modules.qa_mode import ask_question
from modules.vector_db import store_document


st.set_page_config(page_title="AI AudioBook Generator", layout="wide")


# ---------- SESSION STATE ----------
if "rewritten_text" not in st.session_state:
    st.session_state.rewritten_text = ""

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None

if "stored_docs" not in st.session_state:
    st.session_state.stored_docs = set()


# ---------- HEADER ----------
st.title("🎧 AI AudioBook Generator")
st.markdown("### Convert your documents into immersive audiobooks")


# ---------- STYLE ----------
style = st.selectbox(
    "🎙 Narration Style",
    ["Storytelling", "Educational", "Podcast"]
)


# ---------- CACHE TEXT EXTRACTION ----------
@st.cache_data
def cached_extract(file):
    return extract_text(file)


# ---------- FILE UPLOAD ----------
uploaded_files = upload_file()

if uploaded_files:

    if not isinstance(uploaded_files, list):
        uploaded_files = [uploaded_files]

    st.success(f"{len(uploaded_files)} file(s) uploaded")

    for idx, uploaded_file in enumerate(uploaded_files, start=1):

        st.markdown("---")
        st.subheader(f"📂 {uploaded_file.name}")

        uploaded_file.seek(0)

        extracted_text = cached_extract(uploaded_file)

        # ---------- STORE VECTOR DB ----------
        doc_key = uploaded_file.name

        if doc_key not in st.session_state.stored_docs:
            store_document(extracted_text)
            st.session_state.stored_docs.add(doc_key)

        st.write("Text length:", len(extracted_text))

        col1, col2 = st.columns(2)

        # ---------- ORIGINAL TEXT ----------
        with col1:
            st.markdown("### 📄 Original Text")
            st.text_area("Original", extracted_text, height=300)

        # ---------- GENERATE AUDIOBOOK ----------
        with col2:

            if st.button(f"🚀 Generate Audiobook {idx}", key=f"btn_{idx}"):

                progress = st.progress(0)

                with st.spinner("🤖 Rewriting with AI..."):
                    st.session_state.rewritten_text = rewrite_text(extracted_text, style)

                progress.progress(50)

                with st.spinner("🔊 Generating voice..."):
                    st.session_state.audio_file = text_to_speech(
                        st.session_state.rewritten_text
                    )

                progress.progress(100)


# ---------- DISPLAY AUDIOBOOK ----------
if st.session_state.rewritten_text != "":

    st.markdown("### 🎧 Audiobook Text")

    st.text_area("Narration", st.session_state.rewritten_text, height=200)


if st.session_state.audio_file:

    st.audio(st.session_state.audio_file)

    deliver_audio(st.session_state.audio_file)


# ---------- QA SECTION ----------
st.markdown("---")

st.markdown("### 🤖 Ask Questions About This Document")

question = st.text_input("Ask anything from this document")

if st.button("Get Answer"):

    if st.session_state.rewritten_text == "":
        st.warning("Please generate the audiobook first.")

    elif question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            answer = ask_question(st.session_state.rewritten_text, question)

        # Store answer in session (important)
        st.session_state.qa_answer = answer

# ---------- DISPLAY ANSWER ----------
if "qa_answer" in st.session_state:

    st.markdown("### 📘 Answer")
    st.write(st.session_state.qa_answer)

    # ---------- BUTTON FOR AUDIO ----------
    if st.button("🔊 Generate Audio for Answer"):

        from modules.tts import text_to_speech

        with st.spinner("Generating audio for answer..."):
            answer_audio = text_to_speech(st.session_state.qa_answer)

        st.audio(answer_audio)

