"""
Audiobook Generator — UI Styling and Playback.
"""
import base64
import html
import re
import streamlit as st
import streamlit.components.v1 as components

import re
import os
import streamlit as st
import streamlit.components.v1 as components

from ui_1 import init_state, apply_style, MAX_FILE_SIZE_BYTES, MAX_FILE_SIZE_MB
from ui_2 import avatar_html, avatar_audio_synced_html
from gemini_helper import generate_questions_with_gemini
from tts import text_to_speech

def generate_notes(text: str, max_points: int = 10) -> str:
    """Create simple bullet-point notes from the text."""
    clean = re.sub(r"\s+", " ", (text or "")).strip()
    if not clean:
        return "No content available for notes."
    sentences = re.split(r"(?<=[.!?])\s+", clean)
    bullets = [f"- {s.strip()}" for s in sentences if len(s.strip()) > 40]
    return "\n".join(bullets[:max_points]) or f"- {clean[:200]}..."

def render_listen_section() -> None:
    """Render the listen and download UI."""
    if not st.session_state.audio_bytes:
        return

    st.markdown("---")
    st.markdown("<div id='listen-section'></div>", unsafe_allow_html=True)
    st.subheader("3. Listen & Download")
    
    voice_used = st.session_state.get("audio_voice", "US Female")
    audio_val = st.session_state.audio_bytes.getvalue() if hasattr(st.session_state.audio_bytes, "getvalue") else st.session_state.audio_bytes
    is_dark = not st.session_state.get("light_mode", False)
    
    synced_html = avatar_audio_synced_html(voice_used, audio_val, is_dark)
    if synced_html:
        components.html(synced_html, height=320)
    else:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(avatar_html(voice_used), unsafe_allow_html=True)
        with col2:
            st.audio(st.session_state.audio_bytes, format="audio/mp3")

    dl_col, note_col, qs_col, stat_col = st.columns([1, 1, 1, 1])
    
    with dl_col:
        st.download_button(
            "⬇ Download MP3",
            data=st.session_state.audio_bytes,
            file_name=st.session_state.audio_file_name or "audiobook.mp3",
            mime="audio/mpeg",
            use_container_width=True
        )

    source_text = st.session_state.get("summary_text") or st.session_state.get("extracted_text", "")

    with note_col:
        if st.button("📝 Generate notes", use_container_width=True):
            if not source_text.strip():
                st.warning("No text available to generate notes.")
            else:
                st.session_state.notes_text = generate_notes(source_text)
                st.session_state.scroll_target = "notes-section"
                st.rerun()

    with qs_col:
        if st.button("❓ Generate questions", use_container_width=True):
            if not source_text.strip():
                st.warning("No text available to generate questions.")
            else:
                with st.spinner("Generating questions..."):
                    st.session_state.questions_text = generate_questions_with_gemini(
                        source_text,
                        api_key=os.getenv("GEMINI_API_KEY", "")
                    )
                st.session_state.scroll_target = "questions-section"
                st.rerun()
                
    with stat_col:
        word_count = st.session_state.get('audio_word_count', 0)
        duration = st.session_state.get('audio_duration_seconds', 0.0)
        if duration == 0.0 and word_count > 0:
            duration = max(1.0, word_count / 2.5)

        if hasattr(st, 'popover'):
            with st.popover("📊 Statistics", use_container_width=True):
                st.markdown(f"**Word Count:** {word_count:,} words")
                mins = int(duration // 60)
                secs = int(duration % 60)
                st.markdown(f"**Audio Time:** {mins}m {secs}s")
        else:
            if st.button("📊 Statistics", use_container_width=True):
                st.session_state.show_stats = not st.session_state.get("show_stats", False)
                st.rerun()

    if st.session_state.get("show_stats") and not hasattr(st, 'popover'):
        word_count = st.session_state.get('audio_word_count', 0)
        duration = st.session_state.get('audio_duration_seconds', 0.0)
        if duration == 0.0 and word_count > 0:
            duration = max(1.0, word_count / 2.5)
        mins = int(duration // 60)
        secs = int(duration % 60)
        st.info(f"**Word Count:** {word_count:,} words | **Audio Time:** {mins}m {secs}s")

    if st.session_state.get("notes_text"):
        st.markdown("---")
        st.markdown("<div id='notes-section'></div>", unsafe_allow_html=True)
        st.text_area("Generated Notes", st.session_state.notes_text, height=150)
        
        n_col1, n_col2 = st.columns(2)
        with n_col1:
            st.download_button(
                "⬇ Download notes text",
                data=st.session_state.notes_text,
                file_name="notes.txt",
                mime="text/plain",
                use_container_width=True,
                key="dl_notes_text"
            )
        with n_col2:
            if st.button("🎙 Generate Notes Audio", use_container_width=True, key="gen_notes_audio"):
                with st.spinner("Generating audio..."):
                    try:
                        st.session_state.notes_audio_bytes = text_to_speech(
                            st.session_state.notes_text, 
                            voice=voice_used
                        )
                    except Exception as e:
                        st.error(f"Audio generation failed: {e}")

        if st.session_state.get("notes_audio_bytes"):
            st.audio(st.session_state.notes_audio_bytes, format="audio/mp3")
            st.download_button(
                "⬇ Download Notes Audio",
                data=st.session_state.notes_audio_bytes,
                file_name="notes_audio.mp3",
                mime="audio/mpeg",
                use_container_width=True,
                key="dl_notes_audio_btn"
            )

    if st.session_state.get("questions_text"):
        st.markdown("---")
        st.markdown("<div id='questions-section'></div>", unsafe_allow_html=True)
        st.text_area("Generated Questions", st.session_state.questions_text, height=150)
        
        q_col1, q_col2 = st.columns(2)
        with q_col1:
            st.download_button(
                "⬇ Download questions text",
                data=st.session_state.questions_text,
                file_name="questions.txt",
                mime="text/plain",
                use_container_width=True,
                key="dl_qs_text"
            )
        with q_col2:
            if st.button("🎙 Generate Questions Audio", use_container_width=True, key="gen_qs_audio"):
                with st.spinner("Generating audio..."):
                    try:
                        st.session_state.questions_audio_bytes = text_to_speech(
                            st.session_state.questions_text, 
                            voice=voice_used
                        )
                    except Exception as e:
                        st.error(f"Audio generation failed: {e}")

        if st.session_state.get("questions_audio_bytes"):
            st.audio(st.session_state.questions_audio_bytes, format="audio/mp3")
            st.download_button(
                "⬇ Download Questions Audio",
                data=st.session_state.questions_audio_bytes,
                file_name="questions_audio.mp3",
                mime="audio/mpeg",
                use_container_width=True,
                key="dl_qs_audio_btn"
            )

    components.html(
        """
        <script>
            function hideAudioDownload() {
                const parent = window.parent;
                if (!parent || !parent.document) return;
                const audios = parent.document.querySelectorAll('audio');
                audios.forEach(a => {
                    a.setAttribute('controlsList', 'nodownload');
                });
            }
            setTimeout(hideAudioDownload, 100);
            setTimeout(hideAudioDownload, 500);
            setTimeout(hideAudioDownload, 1000);
        </script>
        """,
        height=0
    )

    if st.session_state.get("scroll_target"):
        target = st.session_state.scroll_target
        st.session_state.scroll_target = ""
        components.html(
            f"""
            <script>
                function doScroll() {{
                    const parent = window.parent;
                    // Target specific element ID if available in Streamlit DOM
                    const targetEl = parent.document.getElementById('{target}');
                    if (targetEl) {{
                        targetEl.scrollIntoView({{behavior: 'smooth', block: 'start'}});
                    }} else {{
                        // Fallback to scrolling to bottom
                        const selectors = ['section.main', '[data-testid="stAppViewContainer"]', '.block-container'];
                        let scrolled = false;
                        for (let sel of selectors) {{
                            const el = parent.document.querySelector(sel);
                            if (el) {{
                                el.scrollTo({{top: el.scrollHeight, behavior: 'smooth'}});
                                scrolled = true;
                            }}
                        }}
                        if (!scrolled) {{
                            parent.scrollTo({{top: parent.document.body.scrollHeight, behavior: 'smooth'}});
                        }}
                    }}
                }}
                // Execute with slight delays to ensure DOM is updated
                setTimeout(doScroll, 100);
                setTimeout(doScroll, 500);
            </script>
            """,
            height=0
        )
