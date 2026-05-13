import google.generativeai as genai
import os
from typing import Optional

class LLMService:
    def __init__(self):
        # API Key'i .env dosyasından veya ortam değişkenlerinden alıyoruz
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Hackathon için en hızlı ve dengeli model olan gemini-1.5-flash kullanıyoruz
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            print("⚠️ Uyarı: GEMINI_API_KEY bulunamadı. LLMService kısıtlı modda çalışacak.")

    async def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """
        Genel amaçlı metin üretme fonksiyonu.
        """
        if not self.model:
            return "LLM Service şu an kullanılamıyor. Lütfen API anahtarını kontrol edin."

        try:
            # Eğer sistem talimatı varsa promptun başına ekleyebiliriz veya 
            # modeli başlatırken verebiliriz. En hızlı yol prompt içinde belirtmektir.
            full_prompt = f"{system_instruction}\n\nUser: {prompt}" if system_instruction else prompt
            
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Metin üretilirken bir hata oluştu: {str(e)}"

    async def get_json_response(self, prompt: str):
        """
        AI'dan JSON formatında yanıt almak için kullanılır.
        (Özellikle trend analizi ve rapor özetleri için kritik)
        """
        # Gemini 1.5 Flash JSON mode destekler
        # Not: Prompt içinde 'return JSON' demeyi unutmayın.
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return response.text
        except Exception as e:
            print(f"JSON yanıt hatası: {e}")
            return None

# Singleton Pattern: Sınıfı bir kez örnekliyoruz, her yer buradan kullanıyor.
llm_service = LLMService()