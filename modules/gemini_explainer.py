# modules/gemini_explainer.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ Google API key not found in .env")

genai.configure(api_key=api_key)

# Use a supported Gemini 2.5 model
model = genai.GenerativeModel("gemini-2.5-pro")

def gpt_explain(concept: str) -> str:
    """
    Explains a given concept using Gemini 2.5 Pro.
    """
    prompt = f"Explain the concept of '{concept}' in a simple, clear way for students."
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error while generating explanation: {str(e)}"
