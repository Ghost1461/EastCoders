import json
from datetime import date

from sqlalchemy.orm import Session

from app.services.trend_service import (
    get_market_trends,
    get_personalized_market_trends
)

from app.services.llm_service import generate_text_with_gemini

from app.models.trend_ai_cache_model import TrendAISummaryCache


def safe_parse_json_response(raw_response: str):
    try:
        cleaned = (
            raw_response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(cleaned)

    except Exception:
        return {
            "market_overview": raw_response,
            "personal_opportunities": "",
            "action_suggestions": ""
        }


def generate_trends_ai_summary(
    db: Session,
    current_user,
    limit: int = 20,
    force_refresh: bool = False
):
    today = date.today().isoformat()

    cached = (
        db.query(TrendAISummaryCache)
        .filter(
            TrendAISummaryCache.user_id == current_user.id,
            TrendAISummaryCache.summary_type == "trend_page",
            TrendAISummaryCache.cache_date == today
        )
        .first()
    )

    if cached and not force_refresh:
        return json.loads(cached.summary)

    market_trends = get_market_trends(
        db=db,
        limit=limit
    )

    personalized_trends = get_personalized_market_trends(
        db=db,
        limit=limit
    )

    market_text = []

    for trend in market_trends[:10]:
        extra = trend.get("extra_data") or {}

        market_text.append(
            f"""
Trend: {trend.get("trend_name")}
Kategori: {trend.get("category")}
Trend Score: {trend.get("trend_score")}
Rank: {extra.get("rank")}
Marka: {extra.get("brand")}
Fiyat: {extra.get("price_text")}
Rating: {extra.get("rating")}
Yorum Sayısı: {extra.get("review_count")}
Satış Sinyali: {extra.get("order_count_text")}
Favori Sinyali: {extra.get("favorite_count_text")}
Görüntülenme Sinyali: {extra.get("view_count_text")}
"""
        )

    personalized_text = []

    for item in personalized_trends[:10]:
        trend = item.get("trend") or {}
        matched_products = item.get("matched_products") or []

        matched_product_text = []

        for product in matched_products[:5]:
            matched_product_text.append(
                f"""
Ürün: {product.get("product_name")}
Kategori: {product.get("category")}
Platform: {product.get("platform")}
Fiyat: {product.get("price")}
Stok: {product.get("stock")}
Rating: {product.get("rating")}
Durum: {product.get("status")}
"""
            )

        personalized_text.append(
            f"""
Eşleşen Trend: {trend.get("trend_name")}
Kategori: {trend.get("category")}
Trend Score: {trend.get("trend_score")}
Trend Satış Sinyali: {(trend.get("extra_data") or {}).get("order_count_text")}
Trend Favori Sinyali: {(trend.get("extra_data") or {}).get("favorite_count_text")}
Trend Görüntülenme Sinyali: {(trend.get("extra_data") or {}).get("view_count_text")}

Eşleşen Kullanıcı Ürünleri:
{matched_product_text}
"""
        )

    has_personalized = len(personalized_text) > 0

    prompt = f"""
Sen bir e-ticaret trend analiz uzmanısın.

Aşağıdaki veriler bir seller dashboard'un trend sayfasından geliyor.

Görev:
SADECE geçerli JSON döndür. Markdown, açıklama veya kod bloğu yazma.

JSON formatı kesinlikle şu olsun:

{{
  "market_overview": "...",
  "personal_opportunities": "...",
  "action_suggestions": "..."
}}

Kurallar:
- Her alan maksimum 2 cümle olsun.
- Türkçe yaz.
- "market_overview": piyasada yükselen ürün/kategori trendlerini özetle.
- "personal_opportunities": Eğer kullanıcıya özel eşleşen trendler varsa, trend adlarını ve eşleşen ürün kategorilerini açıkça yaz.
- "personal_opportunities": Eğer aşağıdaki has_personalized değeri true ise kesinlikle "eşleşme yok", "fırsat yok" veya "belirgin fırsat yok" deme.
- "personal_opportunities": Eğer has_personalized true ise en az bir eşleşen trend ve en az bir eşleşen kullanıcı ürün kategorisi belirt.
- "personal_opportunities": Eğer has_personalized false ise kullanıcıya özel fırsat bulunmadığını söyle.
- "action_suggestions": fiyat, stok, başlık, görsel veya reklam açısından uygulanabilir öneri ver.
- Başlık yazma; sadece JSON keylerinin değerlerini doldur.

has_personalized:
{has_personalized}

Market trendleri:
{market_text}

Kullanıcıya özel eşleşen trendler:
{personalized_text}
"""

    raw_summary = generate_text_with_gemini(prompt)
    parsed_summary = safe_parse_json_response(raw_summary)

    parsed_as_text = json.dumps(
        parsed_summary,
        ensure_ascii=False
    ).lower()

    if (
        "kota limiti" not in parsed_as_text
        and "üretilemedi" not in parsed_as_text
    ):
        if cached:
            cached.summary = json.dumps(
                parsed_summary,
                ensure_ascii=False
            )
        else:
            new_cache = TrendAISummaryCache(
                user_id=current_user.id,
                summary_type="trend_page",
                summary=json.dumps(
                    parsed_summary,
                    ensure_ascii=False
                ),
                cache_date=today
            )

            db.add(new_cache)

        db.commit()

    return parsed_summary