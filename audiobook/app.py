import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from text_extractor import extract_text
from llm_processor import enrich_text
from tts_converter import text_to_speech, get_available_voices
from analytics import log_generation, get_summary, get_all_records

# Load environment variables from .env file
load_dotenv()

# Configure page
st.set_page_config(page_title="AudioBook Generator", page_icon="🎧", layout="wide")

# Create output directory
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

st.title("🎧 AudioBook Generator")
st.markdown("Upload documents and convert them into engaging audiobooks!")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Settings")
    use_llm = st.checkbox("Enable LLM Enhancement", value=True)
    
    if use_llm:
        model_choice = st.selectbox(
            "LLM Model",
            [
                "openrouter/free",
                "google/gemini-2.0-flash-exp:free",
                "meta-llama/llama-3.2-3b-instruct:free",
                "qwen/qwen-2.5-7b-instruct:free"
            ],
            index=0,
            help="openrouter/free automatically selects from available free models"
        )
    else:
        model_choice = None
    
    voice_speed = st.slider("Speech Speed", 100, 200, 150)

    available_voices = get_available_voices()
    if available_voices:
        voice_names = list(available_voices.keys())
        # Default to a female voice if present
        default_idx = next(
            (i for i, n in enumerate(voice_names) if any(
                kw in n.lower() for kw in ("zira", "hazel", "female", "susan", "catherine", "victoria", "samantha")
            )),
            0
        )
        selected_voice_name = st.selectbox("🎤 Voice", voice_names, index=default_idx)
        selected_voice_id = available_voices[selected_voice_name]
    else:
        selected_voice_id = None
    
    st.markdown("---")
    st.caption("Built with Streamlit • Powered by Python")
    
tab_gen, tab_analytics = st.tabs(["🎙️ Generate", "📊 Analytics"])

with tab_gen:
    # File upload
    uploaded_files = st.file_uploader(
        "Upload your documents (PDF, DOCX, TXT)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
        
        if st.button("🎙️ Generate AudioBook", type="primary"):
            import time

            progress_bar = st.progress(0, text="Starting...")
            status_text = st.empty()

            def update_progress(pct: float, label: str):
                progress_bar.progress(pct, text=label)
                status_text.text(label)

            combined_text = ""
            start_time = time.time()

            # Step 1 — Extract text
            for idx, uploaded_file in enumerate(uploaded_files):
                pct = (idx + 1) / (len(uploaded_files) * 3)
                update_progress(pct, f"📄 Extracting text from {uploaded_file.name}... ({idx+1}/{len(uploaded_files)})")
                text = extract_text(uploaded_file)
                combined_text += f"\n\n{text}"

            update_progress(0.40, f"📄 Extraction complete — {len(combined_text):,} chars")
            st.info(f"📊 Extracted {len(combined_text):,} characters")

            # Step 2 — LLM Enhancement
            if use_llm:
                update_progress(0.55, "🤖 Enhancing text with LLM...")
                try:
                    combined_text = enrich_text(combined_text, model=model_choice)
                    update_progress(0.75, "✨ LLM enhancement done")
                    st.success("✨ Text enhanced for audiobook narration")
                except Exception as e:
                    st.warning(f"⚠️ LLM enhancement failed: {e}. Using original text.")

            # Step 3 — TTS
            update_progress(0.85, "🎵 Converting to speech...")
            output_file = OUTPUT_DIR / "audiobook.mp3"
            text_to_speech(combined_text, str(output_file), rate=voice_speed, voice_id=selected_voice_id)

            duration = time.time() - start_time
            log_generation(
                files=[f.name for f in uploaded_files],
                char_count=len(combined_text),
                llm_used=use_llm,
                model=model_choice,
                duration_sec=duration
            )

            update_progress(1.0, "✅ AudioBook generated successfully!")

            with open(output_file, "rb") as audio_file:
                st.download_button(
                    label="⬇️ Download AudioBook",
                    data=audio_file,
                    file_name="audiobook.mp3",
                    mime="audio/mpeg"
                )
            st.audio(str(output_file))

    else:
        st.info("👆 Upload one or more documents to get started")

with tab_analytics:
    import pandas as pd

    records = get_all_records()
    summary = get_summary()

    if not records:
        st.info("No runs yet. Generate an audiobook to see analytics.")
    else:
        # ── Key metrics ──────────────────────────────────────────────
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Runs", summary["total_runs"])
        c2.metric("Total Chars Processed", f"{summary['total_chars_processed']:,}")
        c3.metric("Avg Duration (s)", summary["avg_duration_sec"])
        c4.metric("LLM Enhanced Runs", summary["llm_enhanced_runs"])

        st.markdown("---")

        df = pd.DataFrame(records)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["run"] = range(1, len(df) + 1)
        df["model"] = df["model"].fillna("none")

        # ── Charts row 1 ─────────────────────────────────────────────
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Chars Processed per Run")
            st.bar_chart(df.set_index("run")["char_count"])

        with col2:
            st.subheader("Duration per Run (s)")
            st.line_chart(df.set_index("run")["duration_sec"])

        # ── Charts row 2 ─────────────────────────────────────────────
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Model Usage")
            model_df = pd.DataFrame(
                list(summary["model_usage"].items()), columns=["Model", "Count"]
            ).set_index("Model")
            st.bar_chart(model_df)

        with col4:
            st.subheader("LLM vs Plain Runs")
            llm_df = pd.DataFrame({
                "Type": ["LLM Enhanced", "Plain TTS"],
                "Count": [
                    summary["llm_enhanced_runs"],
                    summary["total_runs"] - summary["llm_enhanced_runs"]
                ]
            }).set_index("Type")
            st.bar_chart(llm_df)

        # ── Run history table ─────────────────────────────────────────
        st.subheader("Run History")
        display_df = df[["run", "timestamp", "char_count", "duration_sec", "llm_used", "model", "files"]].copy()
        display_df["files"] = display_df["files"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
        display_df.columns = ["Run", "Timestamp", "Chars", "Duration (s)", "LLM Used", "Model", "Files"]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit • Powered by Python")
