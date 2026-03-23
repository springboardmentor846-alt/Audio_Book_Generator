import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self, api_key=None, model_name='gemini-1.5-flash'):
        if api_key:
            api_key = api_key.strip()
            genai.configure(api_key=api_key)
        elif os.getenv("GOOGLE_API_KEY"):
            env_key = os.getenv("GOOGLE_API_KEY")
            if env_key:
                genai.configure(api_key=env_key.strip())
        
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)

    def get_available_models(self):
        """
        Fetches and returns a list of available models that support generateContent.
        """
        try:
            models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    # Strip 'models/' prefix if present
                    name = m.name.replace('models/', '')
                    models.append(name)
            return models
        except Exception as e:
            return [f"Error listing models: {str(e)}"]

    def rewrite_for_audiobook(self, text, progress_callback=None, narrator_style="Professional"):
        """
        Rewrites the input text into an engaging, audiobook-style narrative.
        Chunks large texts to prevent timeouts and token limits.
        """
        max_chars = 15000 
        
        if len(text) <= max_chars:
            if progress_callback:
                progress_callback(50, "Rewriting text...")
            res = self._rewrite_chunk(text, narrator_style)
            if progress_callback:
                progress_callback(100, "Completed!")
            return res

        chunks = []
        current_chunk = ""
        for paragraph in text.split('\n'):
            if len(current_chunk) + len(paragraph) > max_chars:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n"
            else:
                current_chunk += paragraph + "\n"
                
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
            
        rewritten_chunks = []
        total_chunks = len(chunks)
        
        for i, chunk in enumerate(chunks):
            if progress_callback:
                progress_callback(int((i / total_chunks) * 100), f"Rewriting part {i+1} of {total_chunks}...")
                
            res = self._rewrite_chunk(chunk, narrator_style)
            if res.startswith("Error"):
                return f"Error on part {i+1}: {res}"
                
            rewritten_chunks.append(res)
            
        if progress_callback:
            progress_callback(100, "Completed!")
            
        return "\n\n".join(rewritten_chunks)

    def _rewrite_chunk(self, text, narrator_style):
        style_instructions = {
            "Professional": "The tone should be similar to a professional, articulate narrator telling a story clearly and neutrally.",
            "Dramatic": "The tone should be highly dramatic, suspenseful, and emotionally gripping, like a thriller audiobook.",
            "Bedtime Story": "The tone should be deeply soothing, gentle, and calming, perfect for relaxed listening or falling asleep.",
            "Enthusiastic": "The tone should be highly energetic, upbeat, inspiring, and engaging, keeping the listener extremely motivated.",
            "Comedic": "The tone should be lighthearted, witty, and slightly humorous, making the listener chuckle."
        }
        chosen_style = style_instructions.get(narrator_style, style_instructions["Professional"])

        prompt = f"""
        You are a professional audiobook scriptwriter. Your task is to rewrite the following text to make it sound 
        engaging, descriptive, and easy to listen to. 

        Instructions:
        1. Maintain the original meaning and key information.
        2. Use natural, conversational language.
        3. Break down long, complex sentences into shorter, clearer ones.
        4. Add descriptive language where appropriate to paint a picture for the listener.
        5. Use transitions to create a smooth flow between ideas.
        6. {chosen_style}

        Text to rewrite:
        {text}

        Rewritten Audiobook Script:
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error during rewriting: {str(e)}"
