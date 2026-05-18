import os

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


def get_gemini_model():
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY bulunamadı.")

    genai.configure(api_key=GEMINI_API_KEY)

    return genai.GenerativeModel(GEMINI_MODEL)


def generate_text_with_gemini(prompt: str) -> str:
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)

        return response.text

    except ResourceExhausted:
        return (
            "AI önerisi şu anda kota limiti nedeniyle üretilemedi. "
            "Lütfen kısa bir süre sonra tekrar deneyin."
        )

    except Exception as e:
        print("Gemini error:", e)

        return (
            "AI önerisi şu anda üretilemedi. "
            "Lütfen daha sonra tekrar deneyin."
        )