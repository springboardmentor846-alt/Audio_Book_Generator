import os
from gtts import gTTS

class TTSService:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_audio(self, text, filename="audiobook.mp3", lang='en', tld='com', slow=False):
        """
        Generates an audio file from text using gTTS.
        Supports regional accents via tld and speed control.
        """
        try:
            if not text or not text.strip():
                return "Error: Empty text provided."
                
            tts = gTTS(text=text, lang=lang, tld=tld, slow=slow)
            filepath = os.path.join(self.output_dir, filename)
            tts.save(filepath)
            
            return filepath
        except Exception as e:
            return f"Error generating audio: {str(e)}"
