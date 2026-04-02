import os

import streamlit as st
from groq import Groq


def _load_groq_api_key() -> str:
    """
    Load GROQ_API_KEY from Streamlit secrets or environment variables.
    Shows a Streamlit error and stops the app if the key is missing.
    """
    api_key = ""

    # 1) Try Streamlit secrets
    try:
        if hasattr(st, "secrets") and st.secrets:
            api_key = st.secrets.get("GROQ_API_KEY", "")  # type: ignore[attr-defined]
    except Exception:
        api_key = ""

    # 2) Fallback to environment variable
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY", "")

    if not api_key:
        st.warning("⚠️ GROQ_API_KEY not found - text-enhancing AI features are disabled.")
        st.markdown(
            """
**Please add your Groq API key in one of these ways:**

1. **Create/Edit `.streamlit/secrets.toml` file** (next to `audiobook.py`):
   ```toml
   GROQ_API_KEY = "your_api_key_here"
   ```
   Then restart Streamlit.

2. **Or set as environment variable:**
   ```bash
   # Windows PowerShell:
   $env:GROQ_API_KEY="your_api_key_here"

   # Windows CMD:
   set GROQ_API_KEY=your_api_key_here

   # Linux/Mac:
   export GROQ_API_KEY="your_api_key_here"
   ```

Get your free API key from: https://console.groq.com/
"""
        )
        # Continue running with reduced functionality
        return ""

    return api_key


def create_groq_client() -> "Groq | None":
    """Create and return a configured Groq client (or None if unavailable)."""
    api_key = _load_groq_api_key()
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.warning(f"⚠️ Failed to initialize Groq client: {e}")
        return None


# Shared Groq client instance for the app
client = create_groq_client()  # type: ignore[var-annotated]


