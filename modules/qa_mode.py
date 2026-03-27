import os
from dotenv import load_dotenv
import google.generativeai as genai

from modules.vector_db import retrieve_chunks

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")


def ask_question(context, question):

    try:

        # Retrieve relevant chunks from vector DB
        relevant_chunks = retrieve_chunks(question)

        context = "\n".join(relevant_chunks)

        prompt = f"""
You are an AI tutor helping a student understand a document.

Use the context below to answer the question.

CONTEXT:
{context}

QUESTION:
{question}

Answer clearly and briefly.
"""

        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text

        if hasattr(response, "candidates"):
            return response.candidates[0].content.parts[0].text

        return "No answer generated."

    except Exception as e:
        return f"Error: {str(e)}"