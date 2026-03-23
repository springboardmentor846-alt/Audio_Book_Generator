"""
Audiobook Generator — UI Styling and Configuration (Part 1).
"""
import streamlit as st

# Constants
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
MAX_EMBED_AUDIO_BYTES = 1_300_000

# Avatar emoji and color per voice (for speaking avatar in Listen & Download)
AVATAR_FOR_VOICE: dict[str, tuple[str, str]] = {
    "US Male": ("👨", "#2563eb"),
    "US Female": ("👩", "#db2777"),
    "British Male": ("👨", "#b91c1c"),
    "British Female": ("👩", "#b91c1c"),
    "Indian Male": ("👨", "#ea580c"),
    "Indian Female": ("👩", "#ea580c"),
    "Hindi Male": ("👨", "#ea580c"),
    "Hindi Female": ("👩", "#ea580c"),
    "Child": ("👧", "#059669"),
}

def init_state():
    """Initialize session state variables."""
    defaults = {
        "last_file_name": None,
        "last_file_size": 0,
        "extracted_text": "",
        "audio_bytes": None,
        "audio_file_name": "audiobook.mp3",
        "audio_voice": "US Female",
        "show_preview": False,
        "summary_text": "",
        "summary_method": "",
        "show_summary_preview": False,
        "clean_method": "",
        "notes_text": "",
        "questions_text": "",
        "notes_audio_bytes": None,
        "questions_audio_bytes": None,
        "audio_word_count": 0,
        "audio_duration_seconds": 0.0,
        "show_stats": False,
        "document_language": "English",
        "scroll_target": "",
        "light_mode": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def apply_style():
    """Apply custom CSS for dark/light theme and layout."""
    light = st.session_state.get("light_mode", False)
    if not light:
        # Dark theme: black / blue
        st.markdown(
            """
            <style>
            [data-testid="stHeader"] {display: none;}
            .stApp {
                background: radial-gradient(circle at top, #0f172a 0, #020617 45%, #000000 100%);
                color: #e5e7eb;
            }
            .block-container {
                padding-top: 2rem !important;
                margin-top: 0rem !important;
                padding-bottom: 2rem;
                max-width: 90% !important;
            }
            h1 {
                margin-top: 0rem !important;
                padding-top: 1rem !important;
                font-size: 3rem !important;
                font-weight: 800 !important;
                line-height: 1.2 !important;
                color: #e5e7eb !important;
            }
            h2, h3, h4 {
                color: #cbd5f5 !important;
            }
            /* Language radio labels and Light mode toggle label */
            div[data-testid="stRadio"] > label {
                font-size: 1.5rem !important;
                font-weight: 800 !important;
                margin-bottom: 0.8rem !important;
            }
            div[data-testid="stHorizontalBlock"] div[data-testid="stRadio"] div[role="radiogroup"] {
                gap: 1.5rem !important;
            }
            div[data-testid="stRadio"] label p {
                font-size: 1.5rem !important;
                font-weight: 700 !important;
                color: #ffffff !important;
            }
            div[data-testid="stSlider"] label p,
            div[data-testid="stSelectbox"] label p,
            div[data-testid="stCheckbox"] > label,
            div[data-testid="stCheckbox"] label p,
            div[data-testid="stWidgetLabel"] p {
                font-size: 1.2rem !important;
                color: #ffffff !important;
                font-weight: 800 !important;
            }
            /* Add an outline to the toggle button itself */
            div[data-testid="stCheckbox"] {
                padding: 0.3rem 0.6rem;
                border-radius: 999px;
                border: 1px solid rgba(148, 163, 184, 0.4);
                background: rgba(15, 23, 42, 0.5);
                display: inline-flex;
            }
            /* Upload document area: glassy card with blue glow and fade */
            div[data-testid="stFileUploader"] {
                background: radial-gradient(circle at top, rgba(37,99,235,0.18) 0, rgba(15,23,42,0.95) 55%, #020617 100%);
                border-radius: 16px;
                padding: 1rem 1.2rem 1.1rem 1.2rem;
                border: 1px solid rgba(129,140,248,0.7);
                box-shadow: 0 0 0 1px rgba(30,64,175,0.4), 0 18px 40px rgba(15,23,42,0.9);
                backdrop-filter: blur(16px);
            }
            div[data-testid="stFileUploader"] * {
                color: #e5e7eb !important;
                font-weight: 600;
            }
            div[data-testid="stFileUploader"] button {
                background: #020617 !important;
                border: 1px solid #38bdf8 !important;
                border-radius: 999px !important;
                padding: 0.4rem 1.6rem !important;
            }
            div[data-testid="stFileUploader"] button *, div[data-testid="stFileUploader"] button {
                color: #ffffff !important;
            }
            div[data-testid="stFileUploader"] button:hover {
                background: #0f172a !important;
                border-color: #0ea5e9 !important;
            }
            div[data-testid="stFileUploader"] label p {
                font-size: 0.95rem !important;
                letter-spacing: 0.03em;
                text-transform: uppercase;
                color: #bfdbfe !important;
            }
            div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] {
                border-radius: 12px;
                border: 1px dashed rgba(129,140,248,0.7);
                background: radial-gradient(circle at center, rgba(56,189,248,0.12) 0, transparent 55%);
            }
            div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"]:hover {
                border-color: rgba(96,165,250,0.95);
                box-shadow: 0 0 0 1px rgba(56,189,248,0.5);
            }
            /* Toggle container in top-right */
            .theme-toggle-container {
                position: absolute;
                top: 0.75rem;
                right: 1.5rem;
                z-index: 999;
            }
            div.stButton > button, div.stDownloadButton > button, div[data-testid="stPopover"] button {
                border-radius: 999px;
                padding: 0.4rem 1.6rem !important;
                font-weight: 600 !important;
                border: 1px solid #38bdf8 !important;
                background: #020617 !important;
                color: #e5e7eb !important;
                height: 2.6rem !important;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            div.stButton > button:hover, div.stDownloadButton > button:hover, div[data-testid="stPopover"] button:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 16px rgba(56,189,248,0.35);
                border-color: #0ea5e9 !important;
                color: #f9fafb !important;
                background: #0f172a !important;
            }
            .stTextArea textarea {
                border-radius: 12px;
                border: 1px solid #1f2937;
                background: #020617;
                color: #e5e7eb;
            }
            /* Premium Voice Select Dropdown */
            div[data-baseweb="select"] > div {
                border-radius: 12px !important;
                border: 1px solid rgba(56, 189, 248, 0.4) !important;
                background: linear-gradient(180deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
                transition: all 0.2s ease;
                min-height: 3rem !important;
                align-items: center;
                cursor: pointer;
            }
            div[data-baseweb="select"] div {
                color: #f8fafc !important;
                font-weight: 600 !important;
                font-size: 1.1rem !important;
                line-height: normal !important;
                padding-top: 0.1rem;
            }
            div[data-baseweb="select"] svg {
                color: #38bdf8 !important;
            }
            div[data-baseweb="select"] > div:hover {
                border-color: rgba(56, 189, 248, 0.8) !important;
                box-shadow: 0 0 0 1px rgba(56, 189, 248, 0.5), 0 8px 20px rgba(0, 0, 0, 0.4);
                transform: translateY(-1px);
            }
            /* Popover/Dropdown list styling */
            div[data-baseweb="popover"] > div {
                border-radius: 12px !important;
                background-color: #0f172a !important;
                border: 1px solid rgba(56, 189, 248, 0.4) !important;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.8) !important;
                overflow: hidden !important;
                margin-top: 6px !important;
            }
            ul[role="listbox"] {
                background-color: #0f172a !important;
                padding: 0.5rem !important;
            }
            ul[role="listbox"] li {
                color: #cbd5e1 !important;
                border-radius: 8px !important;
                margin-bottom: 0.3rem !important;
                transition: all 0.2s ease !important;
                padding: 0.8rem 1rem !important;
                font-size: 1rem !important;
                font-weight: 600 !important;
                border: 1px solid transparent;
            }
            ul[role="listbox"] li:hover {
                background-color: rgba(56, 189, 248, 0.15) !important;
                color: #ffffff !important;
                border-color: rgba(56, 189, 248, 0.3);
                transform: translateX(4px);
            }
            ul[role="listbox"] li[aria-selected="true"] {
                background: linear-gradient(90deg, rgba(56, 189, 248, 0.2) 0%, rgba(15, 23, 42, 0) 100%) !important;
                color: #38bdf8 !important;
                border-left: 3px solid #38bdf8 !important;
            }
            /* st.popover styling for constraints */
            div[data-testid="stPopoverBody"] {
                background-color: #0f172a !important;
                border: 1px solid rgba(56, 189, 248, 0.4) !important;
                color: #ffffff !important;
            }
            div[data-testid="stPopoverBody"] p,
            div[data-testid="stPopoverBody"] strong,
            div[data-testid="stPopoverBody"] * {
                color: #ffffff !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Light theme (previous default)
        st.markdown(
            """
            <style>
            [data-testid="stHeader"] {display: none;}
            .block-container {
                padding-top: 2rem !important;
                margin-top: 0rem !important;
                padding-bottom: 2rem;
                max-width: 90% !important;
            }
            .stApp {
                background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
                color: #334155 !important;
            }
            h1 {
                margin-top: 0rem !important;
                padding-top: 1rem !important;
                font-size: 3rem !important;
                font-weight: 800 !important;
                line-height: 1.2 !important;
                color: #0f172a !important;
            }
            h2, h3, h4 {
                color: #1e293b !important;
            }
            div[data-testid="stRadio"] > label {
                font-size: 1.5rem !important;
                font-weight: 800 !important;
                margin-bottom: 0.8rem !important;
            }
            div[data-testid="stHorizontalBlock"] div[data-testid="stRadio"] div[role="radiogroup"] {
                gap: 1.5rem !important;
            }
            div[data-testid="stRadio"] label p {
                font-size: 1.5rem !important;
                font-weight: 700 !important;
                color: #334155 !important;
            }
            div[data-testid="stCheckbox"] > label,
            div[data-testid="stCheckbox"] label p,
            div[data-testid="stWidgetLabel"] p {
                font-size: 1.2rem !important;
                color: #334155 !important;
                font-weight: 800 !important;
            }
            /* Add an outline to the toggle button itself */
            div[data-testid="stCheckbox"] {
                padding: 0.3rem 0.6rem;
                border-radius: 999px;
                border: 1px solid rgba(148, 163, 184, 0.4);
                background: rgba(255, 255, 255, 0.8);
                display: inline-flex;
            }
            /* Styling for the Upload Area in Light Mode */
            div[data-testid="stFileUploader"] {
                background: rgba(255, 255, 255, 0.7);
                border-radius: 16px;
                padding: 1rem 1.2rem 1.1rem 1.2rem;
                border: 1px solid rgba(0, 0, 0, 0.4);
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
                backdrop-filter: blur(12px);
            }
            div[data-testid="stFileUploader"] * {
                color: #1e293b !important;
                font-weight: 600;
            }
            div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] {
                border-radius: 12px;
                border: 2px dashed #000000; /* Black Border */
                background: rgba(241, 245, 249, 0.6);
            }
            div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"]:hover {
                border-color: #0f172a; /* Navy Blue Hover */
                background: rgba(226, 232, 240, 0.8);
            }
            div[data-testid="stFileUploader"] button {
                background: linear-gradient(135deg, #64748b 0%, #334155 100%) !important; /* Grey gradient */
                border: 1px solid #1e293b !important; /* Navy/Dark Grey border */
                border-radius: 999px !important;
                padding: 0.4rem 1.6rem !important;
            }
            div[data-testid="stFileUploader"] button *, div[data-testid="stFileUploader"] button {
                color: #ffffff !important;
            }
            div[data-testid="stFileUploader"] button:hover {
                background: linear-gradient(135deg, #334155 0%, #0f172a 100%) !important; /* Navy gradient */
                box-shadow: 0 4px 12px rgba(15, 23, 42, 0.3);
            }
            /* Regular buttons, download buttons, and popover buttons */
            div.stButton > button, div.stDownloadButton > button, div[data-testid="stPopover"] button {
                border-radius: 999px;
                padding: 0.6rem 1.5rem !important;
                font-weight: 700 !important;
                transition: all 0.2s ease;
                border: 1px solid #000000 !important; /* Black Border */
                background-color: #ffffff !important;
                color: #1e293b !important;
                height: 3rem !important;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            }
            div.stButton > button:hover, div.stDownloadButton > button:hover, div[data-testid="stPopover"] button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 16px rgba(15, 23, 42, 0.15);
                border-color: #0f172a !important; /* Navy border */
                color: #ffffff !important;
                background: linear-gradient(135deg, #64748b 0%, #334155 100%) !important;
            }
            .stTextArea textarea {
                border-radius: 12px;
                border: 1px solid rgba(0, 0, 0, 0.4);
                background: rgba(255, 255, 255, 0.8);
                color: #334155;
            }
            /* Voice select: pill dropdown */
            div[data-baseweb="select"] > div {
                border-radius: 999px !important;
                border: 1px solid #000000 !important;
                background: rgba(255, 255, 255, 0.9) !important;
                box-shadow: 0 2px 6px rgba(0,0,0,0.02);
            }
            div[data-baseweb="select"] div {
                color: #1e293b !important;
            }
            div[data-baseweb="select"] > div:hover {
                border-color: #0f172a !important; /* Navy blue */
                box-shadow: 0 4px 12px rgba(15, 23, 42, 0.1);
            }
            /* st.popover styling for constraints */
            div[data-testid="stPopoverBody"] {
                background-color: #ffffff !important;
                border: 1px solid rgba(0, 0, 0, 0.4) !important;
                color: #1e293b !important;
            }
            div[data-testid="stPopoverBody"] p,
            div[data-testid="stPopoverBody"] strong,
            div[data-testid="stPopoverBody"] * {
                color: #1e293b !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
