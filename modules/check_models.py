import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print("Loaded API Key:", api_key)

genai.configure(api_key=api_key)

for model in genai.list_models():
    print(model.name)