"""
Quick test script to verify secrets.toml is being read correctly.
Run this before running the main app.
"""
import streamlit as st

st.title("Secrets Test")

try:
    if hasattr(st, 'secrets') and st.secrets:
        api_key = st.secrets.get("GROQ_API_KEY", "")
        if api_key:
            st.success(f"✅ GROQ_API_KEY found! (Length: {len(api_key)} characters)")
            st.info(f"First 10 chars: {api_key[:10]}...")
        else:
            st.error("❌ GROQ_API_KEY is empty in secrets.toml")
    else:
        st.error("❌ Cannot access st.secrets")
except Exception as e:
    st.error(f"❌ Error reading secrets: {str(e)}")
    st.info("Make sure you're running Streamlit from the correct directory.")
