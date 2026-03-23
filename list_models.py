import google.generativeai as genai
import os
import sys

api_key = sys.argv[1] if len(sys.argv) > 1 else os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("No API key provided.")
    sys.exit(1)

genai.configure(api_key=api_key)

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")
