"""Module for audio delivery and download."""


def deliver_audio(audio_file):
    """
    Provide audio file for download through Streamlit.
    
    Args:
        audio_file: Audio file object (BytesIO or similar).
    
    Returns:
        bool: True if delivery was successful, False otherwise.
    """
    import streamlit as st
    
    if audio_file is None:
        return False
    
    try:
        st.download_button(
            label="📥 Download AudioBook",
            data=audio_file,
            file_name="audiobook.wav",
            mime="audio/wav"
        )
        st.success("✓ Audio is ready for download!")
        return True
    
    except Exception as e:
        st.error(f"Error delivering audio: {str(e)}")
        return False
