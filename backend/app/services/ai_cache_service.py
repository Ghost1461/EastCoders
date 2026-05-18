import json
import hashlib

from app.models.ai_report_cache_model import AiReportCache
from app.services.gemini_llm_service import generate_gemini_response

## Hash üret, db cache bak, varsa eski ai_response dön, yoksa Gemini'a git, cache'e kaydet, response dön

def create_input_hash(data: dict) -> str:
    normalized_data = json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        default=str
    )

    return hashlib.sha256(
        normalized_data.encode("utf-8")
    ).hexdigest()


def get_cached_or_generate_ai(
    db,
    user_id: int,
    report_type: str,
    input_data: dict,
    prompt: str
):
    input_hash = create_input_hash(input_data)

    cached_response = db.query(AiReportCache).filter(
        AiReportCache.user_id == user_id,
        AiReportCache.report_type == report_type,
        AiReportCache.input_hash == input_hash
    ).first()

    if cached_response:
        return {
            "ai": cached_response.ai_response,
            "from_cache": True,
            "input_hash": input_hash
        }

    ai_response = generate_gemini_response(prompt)

    #String dönmek için cache'e
    if isinstance(ai_response, dict):
        ai_response = ai_response.get("ai_summary") or json.dumps(
            ai_response,
            ensure_ascii=False
        )

    new_cache = AiReportCache(
        user_id=user_id,
        report_type=report_type,
        input_hash=input_hash,
        ai_response=ai_response
    )

    db.add(new_cache)
    db.commit()

    return {
        "ai": ai_response,
        "from_cache": False,
        "input_hash": input_hash
    }