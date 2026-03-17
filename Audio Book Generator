import streamlit as st
import io
import os
from modules.llm_service import LLMService
from modules.tts_service import TTSService
from modules.extractor import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt

def main():
    st.set_page_config(page_title="Audiobook Generator", page_icon="🎧", layout="wide")
    
    # Custom CSS for the new Dark Glassmorphic UI
    st.markdown("""
        <style>
        /* Base Background */
        .stApp {
            background: linear-gradient(135deg, #0e0e0e 0%, #1a1a2e 100%);
            color: #E0E0E0;
        }

        /* Glassmorphic Cards for main containers */
        div[data-testid="stVerticalBlock"] > div {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            padding: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }
        
        div.stButton > button:first-child {
            background: linear-gradient(90deg, #7F56D9 0%, #9b72ec 100%);
            border-radius: 20px;
            padding: 10px 24px;
            font-weight: bold;
            color: white;
            border: none;
            transition: all 0.3s ease-in-out;
        }
        
        div.stButton > button:first-child:hover {
            transform: scale(1.05);
            box-shadow: 0px 0px 15px rgba(127, 86, 217, 0.6);
        }
        
        /* Rounded inputs and text areas with glass feel */
        div.stTextInput input, div.stTextArea textarea, section[data-testid="stFileUploadDropzone"] {
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: white !important;
        }
        
        /* Typography */
        h1, h2, h3 {
            font-weight: 800 !important;
            letter-spacing: -0.5px;
            background: -webkit-linear-gradient(#fff, #bbb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display Logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; padding-top: 20px;">
                <div style="display: flex; justify-content: center; align-items: flex-end; height: 20px; gap: 3px; margin-bottom: 5px;">
                    <div style="width: 3px; height: 20%; background-color: #FF4B4B; border-radius: 2px; animation: bounce 1.2s infinite ease-in-out;"></div>
                    <div style="width: 3px; height: 50%; background-color: #FF4B4B; border-radius: 2px; animation: bounce 1.2s infinite ease-in-out 0.1s;"></div>
                    <div style="width: 3px; height: 100%; background-color: #FF4B4B; border-radius: 2px; animation: bounce 1.2s infinite ease-in-out 0.2s;"></div>
                    <div style="width: 3px; height: 60%; background-color: #FF4B4B; border-radius: 2px; animation: bounce 1.2s infinite ease-in-out 0.3s;"></div>
                    <div style="width: 3px; height: 30%; background-color: #FF4B4B; border-radius: 2px; animation: bounce 1.2s infinite ease-in-out 0.4s;"></div>
                </div>
                <div style="background: rgba(255, 75, 75, 0.1); color: #FF4B4B; padding: 4px 10px; border-radius: 10px; font-size: 14px; font-weight: bold; border: 1px solid rgba(255, 75, 75, 0.3);">
                    ✨ AI Voice Ready
                </div>
            </div>
            <style>
                @keyframes bounce {
                    0%, 100% { transform: scaleY(0.4); }
                    50% { transform: scaleY(1.2); }
                }
            </style>
        """, unsafe_allow_html=True)
    with col2:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
    with col3:
        if os.path.exists("header_image.jpg"):
            st.image("header_image.jpg", use_container_width=True)
            
    st.title("🎧 Audiobook Generator")
    st.markdown("Convert your documents into engaging, audiobook-style narratives.")

    # Sidebar for API Configuration
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API key.")
        
        available_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
        model_choice = "gemini-1.5-flash"

        if api_key:
            if st.button("🔄 Fetch Available Models"):
                with st.spinner("Connecting to Google AI..."):
                    llm_temp = LLMService(api_key=api_key)
                    fetched_models = llm_temp.get_available_models()
                    if fetched_models and not fetched_models[0].startswith("Error"):
                        st.session_state.available_models = fetched_models
                        st.success(f"Found {len(fetched_models)} models!")
                    else:
                        st.error(fetched_models[0])
            
            if 'available_models' in st.session_state:
                available_models = st.session_state.available_models
            
            model_choice = st.selectbox("Select Model", available_models, index=0)

        st.info("You can get an API key from [Google AI Studio](https://aistudio.google.com/)")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Step 1: Upload & Extract")
        uploaded_file = st.file_uploader("Choose a document", type=["pdf", "docx", "txt"])
        
        extracted_text = ""
        if uploaded_file is not None:
            st.info(f"File uploaded: {uploaded_file.name}")
            file_extension = uploaded_file.name.split(".")[-1].lower()
            
            try:
                with st.spinner('Extracting text...'):
                    if file_extension == "pdf":
                        extracted_text = extract_text_from_pdf(uploaded_file)
                    elif file_extension == "docx":
                        extracted_text = extract_text_from_docx(uploaded_file)
                    elif file_extension == "txt":
                        extracted_text = extract_text_from_txt(uploaded_file)
                
                st.success("Text extracted successfully!")
                st.text_area("Extracted Content", extracted_text, height=400)
            except Exception as e:
                st.error(f"An error occurred during extraction: {e}")

    with col2:
        st.subheader("Step 2: Rewrite for Audiobook")
        
        narrator_style = st.selectbox(
            "Select Narrator Style", 
            ["Professional", "Dramatic", "Bedtime Story", "Enthusiastic", "Comedic"],
            index=0
        )
        
        if extracted_text:
            if st.button("✨ Rewrite with LLM"):
                if not api_key or not api_key.strip():
                    st.warning("Please enter your Gemini API Key in the sidebar.")
                else:
                    llm_service = LLMService(api_key=api_key.strip(), model_name=model_choice)
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    def update_progress(percent, message):
                        progress_bar.progress(percent)
                        status_text.text(message)

                    with st.spinner(f'Rewriting using {model_choice} ({narrator_style})...'):
                        rewritten_text = llm_service.rewrite_for_audiobook(
                            extracted_text, 
                            progress_callback=update_progress,
                            narrator_style=narrator_style
                        )
                        
                        if rewritten_text.startswith("Error"):
                            st.error(rewritten_text)
                        else:
                            st.subheader("Rewritten Narrative:")
                            st.session_state.rewritten_text = rewritten_text
                            st.text_area("Audiobook Script", rewritten_text, height=400)
                            st.download_button(
                                label="Download Script",
                                data=rewritten_text,
                                file_name="audiobook_script.txt",
                                mime="text/plain"
                            )
        else:
            st.info("Upload and extract text first to enable rewriting.")

    st.divider()
    st.subheader("Step 3: Listen & Download Audio")
    
    if "rewritten_text" in st.session_state and st.session_state.rewritten_text:
        col_audio1, col_audio2 = st.columns(2)
        with col_audio1:
            accents = {
                "US English": "com",
                "UK English": "co.uk",
                "Australian English": "com.au",
                "Indian English": "co.in",
                "South African English": "co.za"
            }
            selected_accent = st.selectbox("Select Regional Accent", list(accents.keys()), index=0)
        
        with col_audio2:
            st.write("")
            st.write("")
            slow_speed = st.checkbox("Slow Speed Output")

        if st.button("🎧 Generate Audio"):
            with st.spinner(f"Generating {selected_accent} audio..."):
                tts_service = TTSService()
                audio_path = tts_service.generate_audio(
                    st.session_state.rewritten_text, 
                    tld=accents[selected_accent], 
                    slow=slow_speed
                )
                
                if audio_path.startswith("Error"):
                    st.error(audio_path)
                else:
                    st.success("Audio generated successfully!")
                    st.audio(audio_path, format="audio/mp3")
                    
                    with open(audio_path, "rb") as file:
                        btn = st.download_button(
                            label="Download MP3",
                            data=file,
                            file_name="audiobook.mp3",
                            mime="audio/mp3"
                        )
    else:
        st.info("Follow Step 1 and Step 2 to generate the script first before generating audio.")

if __name__ == "__main__":
    main()
