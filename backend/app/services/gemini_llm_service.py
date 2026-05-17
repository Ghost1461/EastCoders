import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def generate_gemini_response(prompt: str):
    if not GEMINI_API_KEY:
        return {
            "error": "GEMINI_API_KEY bulunamadı."
        }

    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel(GEMINI_MODEL)

    response = model.generate_content(prompt)

    return {
        "ai_summary": response.text
    }