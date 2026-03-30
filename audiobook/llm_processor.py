import os

def enrich_text(text, max_chars=3000, model=None):
    """Enhance text using LLM for audiobook narration"""
    
    # Truncate if too long (for demo purposes)
    if len(text) > max_chars:
        text = text[:max_chars] + "..."
    
    # Try OpenRouter first
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        return enrich_with_openrouter(text, api_key, model)
    
    # Try OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return enrich_with_openai(text, api_key)
    
    # Try Gemini
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return enrich_with_gemini(text, api_key)
    
    # Fallback: return original text
    raise Exception("No API key found. Set OPENROUTER_API_KEY, OPENAI_API_KEY or GEMINI_API_KEY environment variable")

def enrich_with_openrouter(text, api_key, model=None):
    """Use OpenRouter API to enhance text"""
    if model is None:
        model = "openrouter/free"  # Auto-selects from available free models
    
    try:
        from openai import OpenAI
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": f"You are an expert audiobook narrator. Rewrite the following text to be more engaging and suitable for audio narration. Keep the content accurate but make it flow naturally when spoken aloud.\n\nText:\n{text}"}
            ],
            max_tokens=4000
        )
        
        return response.choices[0].message.content
    except ImportError:
        raise ImportError("openai package not installed. Run: pip install openai")

def enrich_with_openai(text, api_key):
    """Use OpenAI API to enhance text"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert audiobook narrator. Rewrite the following text to be more engaging and suitable for audio narration. Keep the content accurate but make it flow naturally when spoken aloud."},
                {"role": "user", "content": text}
            ],
            max_tokens=4000
        )
        
        return response.choices[0].message.content
    except ImportError:
        raise ImportError("openai package not installed. Run: pip install openai")

def enrich_with_gemini(text, api_key):
    """Use Google Gemini API to enhance text"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Rewrite this text for an engaging audiobook narration. Keep it accurate but make it flow naturally when spoken:\n\n{text}"
        
        response = model.generate_content(prompt)
        return response.text
    except ImportError:
        raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
