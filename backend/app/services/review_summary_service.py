from app.services.llm_service import llm_service

async def summarize_reviews(product_name, reviews_list):
    prompt = f"{product_name} ürününe gelen şu yorumları analiz et: {reviews_list}"
    instruction = "Sen bir moda e-ticaret uzmanısın. Yorumlardaki ana sorunları ve olumlu yanları 3 cümleyle özetle."
    
    summary = await llm_service.generate_text(prompt, system_instruction=instruction)
    return summary