import os
import time
import tempfile

import streamlit as st
from dotenv import load_dotenv

from modules.extractor import extract_text, chunk_text
from modules.llm_enrichment import enrich_text_standard, enrich_text_dramatized
from modules.llm_auto import get_active_provider
from modules.tts_converter import run_tts_standard, run_tts_dramatized, regenerate_and_remerge, AVAILABLE_VOICES
from modules.qa_auditor import audit_segments, audit_single_file, QAIssue
from modules.audio_delivery import (
    read_audio_bytes,
    cleanup_temp_segments,
    ensure_directory,
    list_previous_audiobooks,
)
load_dotenv()

OUTPUT_DIR = "output"
TEMP_DIR = os.path.join(OUTPUT_DIR, "temp_segments")
ensure_directory(OUTPUT_DIR)
ensure_directory(TEMP_DIR)

# ── Session state for QA persistence across reruns ────────────────────────────
for _key in ("qa_ready", "qa_issues", "qa_mode", "qa_output_path",
             "qa_narrator_voice", "qa_dramatized_script",
             "qa_segment_paths", "qa_scene_texts", "qa_enriched_text",
             "qa_use_ambience", "qa_ambience_volume_db"):
    if _key not in st.session_state:
        st.session_state[_key] = None

st.set_page_config(
    page_title="AudioBook Generator",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Header banner */
    .app-header {
        text-align: center;
        padding: 28px 20px 22px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 14px;
        color: white;
        margin-bottom: 24px;
    }
    .app-header h1 { margin: 0 0 6px; font-size: 2.4rem; }
    .app-header p  { margin: 0; opacity: 0.88; font-size: 1rem; }

    /* Innovative feature callout */
    .innovation-box {
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
        border-left: 4px solid #764ba2;
        border-radius: 8px;
        padding: 14px 16px;
        margin: 12px 0;
    }
    .innovation-box h4 { margin: 0 0 6px; color: #764ba2; }
    .innovation-box p  { margin: 0; font-size: 0.88rem; color: #444; }

    /* Badge */
    .badge {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    /* Scene preview table */
    .scene-row {
        background: #f8f9fa;
        border-radius: 6px;
        padding: 8px 12px;
        margin: 4px 0;
        font-size: 0.87rem;
    }

    /* File card */
    .file-card {
        background: #f0f2f6;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="app-header">
    <h1>🎧 AudioBook Generator</h1>
    <p>Transform your documents into high-quality audiobooks powered by AI</p>
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.header("⚙️ Configuration")

    st.subheader("🎙️ Narrator Voice")
    selected_voice_label = st.selectbox("Voice", list(AVAILABLE_VOICES.keys()))
    selected_voice = AVAILABLE_VOICES[selected_voice_label]

    st.divider()

    st.subheader("🎬 Generation Mode")
    mode = st.radio(
        "Select mode",
        ["Standard", "Dramatized"],
        captions=[
            "Single narrator, clean audiobook prose",
            "Multi-character, emotion-aware voices",
        ],
    )

    if mode == "Dramatized":
        st.divider()
        st.subheader("🎵 Ambient Soundscapes")
        use_ambience = st.toggle(
            "Enable ambient soundscapes",
            value=False,
            help="Mixes procedurally generated emotion-matched ambient audio under each scene.",
        )
        ambience_volume_db = -22
        if use_ambience:
            ambience_volume_db = st.slider(
                "Ambience volume (dBFS)",
                min_value=-35,
                max_value=-10,
                value=-22,
                step=1,
                help="Lower value = quieter ambience. –22 dB is subtle; –12 dB is clearly audible.",
            )
            st.caption(
                "🎼 Each scene gets a unique soundscape: "
                "dark rumble for tense/sad, bright shimmer for excited/happy, "
                "deep throb for mysterious."
            )
    else:
        use_ambience = False
        ambience_volume_db = -22

    st.divider()

    active = get_active_provider()
    provider_labels = {"gemini": "Google Gemini", "groq": "Groq", "openai": "OpenAI", "none": "None configured"}
    st.caption(f"AI Provider: **{provider_labels.get(active, active)}** (auto-selected)")
    st.caption("AudioBook Generator v1.0 | Powered by Edge TTS + AI")

left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("📂 Upload Documents")
    uploaded_files = st.file_uploader(
        "Drag & drop or click to upload",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="Supports PDF, DOCX, and TXT files. Multiple files are merged before processing.",
    )

    if uploaded_files:
        for uf in uploaded_files:
            size_kb = len(uf.getvalue()) / 1024
            st.markdown(
                f'<div class="file-card">📄 <b>{uf.name}</b> &nbsp;·&nbsp; {size_kb:.1f} KB</div>',
                unsafe_allow_html=True,
            )

with right:
    st.subheader("ℹ️ Mode Details")

    if mode == "Standard":
        st.markdown("""
        **Standard Mode** rewrites your document in engaging audiobook prose
        and narrates it with the voice you selected.

        - Single narrator voice
        - LLM rewrites text for natural listening flow
        - Best for articles, reports, and non-fiction
        """)
    else:
        st.markdown("""
        <div class="innovation-box">
            <span class="badge">INNOVATIVE FEATURE</span>
            <h4>Dramatized Audiobook Mode</h4>
            <p>
                The AI analyses your text to detect <b>characters</b>, <b>dialogue</b>,
                and <b>emotional tone</b> per scene. Each character is assigned a unique
                neural voice (different accent &amp; gender). Speaking rate and pitch are
                adjusted per scene to match the detected emotion — turning any document
                into a fully cast, emotionally dynamic audio drama.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if use_ambience:
            st.markdown("""
            <div class="innovation-box">
                <span class="badge">NEW FEATURE</span>
                <h4>Ambient Soundscapes Active</h4>
                <p>
                    Each scene receives a procedurally generated ambient layer matched
                    to its detected emotion — dark rumble for tense/fearful, bright shimmer
                    for excited/happy, slow pulse for mysterious. Generated entirely offline
                    using pink noise + FFT bandpass shaping.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Voice assignments in Dramatized Mode"):
            st.markdown("""
            | Emotion | Effect |
            |---------|--------|
            | happy / excited | Faster rate, higher pitch |
            | sad / fearful | Slower rate, lower pitch |
            | angry / tense | Faster rate, deeper pitch |
            | mysterious | Slower rate, lower pitch |
            | neutral | Default rate and pitch |

            Characters are automatically given distinct voices from a pool of
            8 international English neural voices (US, UK, AU, CA, IN).
            """)

st.divider()

can_generate = bool(uploaded_files)

if not uploaded_files:
    st.info("Upload at least one document to get started.")

if can_generate:
    if st.button("🎧 Generate AudioBook", type="primary", use_container_width=True):

        progress = st.progress(0, text="Starting…")
        status = st.empty()

        status.info("📖 Step 1/3 — Extracting text from documents…")
        progress.progress(10, text="Extracting text…")

        all_text = ""
        try:
            for uf in uploaded_files:
                suffix = "." + uf.name.rsplit(".", 1)[-1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uf.getvalue())
                    tmp_path = tmp.name
                file_type = uf.name.rsplit(".", 1)[-1].lower()
                all_text += extract_text(tmp_path, file_type) + "\n\n"
                os.unlink(tmp_path)
        except Exception as e:
            st.error(f"Text extraction failed: {e}")
            st.stop()

        char_count = len(all_text)
        word_count = len(all_text.split())
        st.success(f"Extracted **{word_count:,} words** ({char_count:,} characters) from {len(uploaded_files)} file(s).")

        status.info("🤖 Step 2/3 — AI is enriching the text… (this may take 15–60 seconds)")
        progress.progress(35, text="LLM processing…")

        enriched_text = None
        dramatized_script = None

        try:
            if mode == "Standard":
                enriched_text = enrich_text_standard(all_text)
                with st.expander("📝 Preview enriched narration"):
                    preview = enriched_text[:1200] + ("…" if len(enriched_text) > 1200 else "")
                    st.text_area("", preview, height=220, label_visibility="collapsed")
            else:
                dramatized_script = enrich_text_dramatized(all_text)
                scenes = dramatized_script.get("scenes", [])
                title = dramatized_script.get("title", "—")

                with st.expander(f"📝 Dramatized script preview — \"{title}\" ({len(scenes)} scenes)"):
                    for scene in scenes[:8]:
                        char = scene.get("character", "NARRATOR")
                        emotion = scene.get("emotion", "neutral")
                        text_preview = scene.get("text", "")[:120]
                        st.markdown(
                            f'<div class="scene-row">'
                            f'<b>{char}</b> &nbsp;<span style="color:#888">({emotion})</span>'
                            f'&nbsp;— {text_preview}{"…" if len(scene.get("text","")) > 120 else ""}'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                    if len(scenes) > 8:
                        st.caption(f"… and {len(scenes) - 8} more scenes")

        except Exception as e:
            st.error(f"LLM enrichment failed: {e}")
            st.stop()

        ambience_label = " + mixing ambient soundscapes" if (mode == "Dramatized" and use_ambience) else ""
        status.info(f"🔊 Step 3/4 — Converting to speech{ambience_label}… (this may take 20–90 seconds)")
        progress.progress(65, text="Generating audio…")

        output_filename = f"audiobook_{int(time.time())}.mp3"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        try:
            if mode == "Standard":
                run_tts_standard(enriched_text, output_path, selected_voice)
            else:
                cleanup_temp_segments(TEMP_DIR)
                run_tts_dramatized(
                    dramatized_script, TEMP_DIR, output_path, selected_voice,
                    use_ambience=use_ambience,
                    ambience_volume_db=float(ambience_volume_db),
                )
        except Exception as e:
            st.error(f"TTS conversion failed: {e}")
            st.stop()

        # ── Step 4: QA Audit ──────────────────────────────────────────────────
        progress.progress(90, text="Running QA audit…")
        status.info("🔍 Step 4/4 — Running auto QA audit on generated audio…")

        try:
            if mode == "Standard":
                qa_issues = audit_single_file(output_path, enriched_text)
            else:
                scenes_list = dramatized_script.get("scenes", [])
                scene_texts = [s.get("text", "").strip() for s in scenes_list]
                seg_paths   = [
                    os.path.join(TEMP_DIR, f"seg_{i:04d}.mp3")
                    for i, t in enumerate(scene_texts) if t
                ]
                seg_texts   = [t for t in scene_texts if t]
                qa_issues   = audit_segments(seg_paths, seg_texts)

                # Store state needed for Fix button
                st.session_state.qa_segment_paths   = seg_paths
                st.session_state.qa_scene_texts     = seg_texts
                st.session_state.qa_dramatized_script = dramatized_script

            st.session_state.qa_issues            = qa_issues
            st.session_state.qa_mode              = mode
            st.session_state.qa_output_path       = output_path
            st.session_state.qa_narrator_voice    = selected_voice
            st.session_state.qa_enriched_text     = enriched_text if mode == "Standard" else None
            st.session_state.qa_use_ambience      = use_ambience
            st.session_state.qa_ambience_volume_db = float(ambience_volume_db)
            st.session_state.qa_ready             = True
        except Exception:
            st.session_state.qa_ready = False  # QA failed silently; don't block delivery

        progress.progress(100, text="Done!")
        status.success("AudioBook generated successfully!")

        st.divider()
        st.subheader("🎉 Your AudioBook is Ready!")

        audio_bytes = read_audio_bytes(output_path)
        file_size_mb = len(audio_bytes) / (1024 * 1024)

        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.audio(audio_bytes, format="audio/mp3")
        with col_b:
            st.metric("File size", f"{file_size_mb:.2f} MB")
            st.metric("Mode", mode)

        st.download_button(
            label="⬇️ Download AudioBook (.mp3)",
            data=audio_bytes,
            file_name=output_filename,
            mime="audio/mpeg",
            use_container_width=True,
            type="primary",
        )
# ── QA Report Section ─────────────────────────────────────────────────────────
if st.session_state.qa_ready and st.session_state.qa_issues is not None:
    st.divider()
    qa_issues: list[QAIssue] = st.session_state.qa_issues
    errors   = [i for i in qa_issues if i.severity == "error"]
    warnings = [i for i in qa_issues if i.severity == "warning"]

    st.subheader("🔍 Auto QA Report")

    if not qa_issues:
        st.success("✅ All segments passed QA checks — no issues detected.")
    else:
        col_e, col_w, col_t = st.columns(3)
        col_e.metric("Errors",   len(errors),   delta=None)
        col_w.metric("Warnings", len(warnings), delta=None)
        col_t.metric("Total Segments Checked",
                     len(st.session_state.qa_segment_paths or [1]))

        _ISSUE_ICONS = {
            "EMPTY":        ("🔴", "Generation failed — segment is empty or missing"),
            "TRUNCATED":    ("🔴", "Audio cut off mid-sentence"),
            "HALLUCINATED": ("🟡", "Audio longer than expected — possible LLM padding"),
            "HIGH_SILENCE": ("🟡", "Excessive silence — possible TTS glitch"),
        }

        with st.expander(f"View {len(qa_issues)} issue(s)", expanded=True):
            for issue in qa_issues:
                icon, label = _ISSUE_ICONS.get(issue.issue_type, ("⚪", issue.issue_type))
                seg_label = (
                    f"Segment #{issue.segment_index}"
                    if st.session_state.qa_mode == "Dramatized"
                    else "Full audio file"
                )
                st.markdown(
                    f"{icon} **{seg_label}** &nbsp;·&nbsp; `{issue.issue_type}` — {issue.details}",
                    unsafe_allow_html=True,
                )

        # ── Fix buttons ───────────────────────────────────────────────────────
        fixable = [i for i in qa_issues if i.severity == "error"]

        if fixable and st.session_state.qa_mode == "Dramatized":
            if st.button(
                f"🔧 Fix {len(fixable)} Bad Segment(s) & Remerge",
                type="primary",
                use_container_width=True,
            ):
                bad_indices = [i.segment_index for i in fixable]
                with st.spinner(f"Regenerating {len(bad_indices)} segment(s)…"):
                    try:
                        new_path = regenerate_and_remerge(
                            bad_indices=bad_indices,
                            script=st.session_state.qa_dramatized_script,
                            temp_dir=TEMP_DIR,
                            final_output=st.session_state.qa_output_path,
                            narrator_voice=st.session_state.qa_narrator_voice,
                            use_ambience=st.session_state.qa_use_ambience or False,
                            ambience_volume_db=st.session_state.qa_ambience_volume_db or -22.0,
                        )
                        # Re-run QA on fixed segments
                        re_issues = audit_segments(
                            st.session_state.qa_segment_paths,
                            st.session_state.qa_scene_texts,
                        )
                        st.session_state.qa_issues = re_issues
                        st.success(f"Fixed! Remaining issues after re-audit: {len(re_issues)}")
                        fixed_bytes = read_audio_bytes(new_path)
                        st.audio(fixed_bytes, format="audio/mp3")
                        st.download_button(
                            "⬇️ Download Fixed AudioBook (.mp3)",
                            data=fixed_bytes,
                            file_name=os.path.basename(new_path),
                            mime="audio/mpeg",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"Fix failed: {e}")

        elif fixable and st.session_state.qa_mode == "Standard":
            if st.button(
                "🔧 Regenerate Full AudioBook",
                type="primary",
                use_container_width=True,
            ):
                with st.spinner("Regenerating…"):
                    try:
                        run_tts_standard(
                            st.session_state.qa_enriched_text,
                            st.session_state.qa_output_path,
                            st.session_state.qa_narrator_voice,
                        )
                        re_issues = audit_single_file(
                            st.session_state.qa_output_path,
                            st.session_state.qa_enriched_text,
                        )
                        st.session_state.qa_issues = re_issues
                        st.success(f"Regenerated! Remaining issues: {len(re_issues)}")
                        fixed_bytes = read_audio_bytes(st.session_state.qa_output_path)
                        st.audio(fixed_bytes, format="audio/mp3")
                        st.download_button(
                            "⬇️ Download Fixed AudioBook (.mp3)",
                            data=fixed_bytes,
                            file_name=os.path.basename(st.session_state.qa_output_path),
                            mime="audio/mpeg",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"Regeneration failed: {e}")

previous = list_previous_audiobooks(OUTPUT_DIR)
if previous:
    st.divider()
    with st.expander(f"📚 Previously Generated AudioBooks ({len(previous)} files)"):
        for entry in previous:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"🎵 {entry['name']} — {entry['size_kb']} KB")
            with col2:
                audio_data = read_audio_bytes(entry["path"])
                st.download_button(
                    "Download",
                    data=audio_data,
                    file_name=entry["name"],
                    mime="audio/mpeg",
                    key=f"dl_{entry['name']}",
                )
