import uuid
from datetime import datetime
import requests
from sqlalchemy.orm import Session

from app.core.config import NEWS_API_KEY
from app.models import MarketNews


NEWS_API_URL = "https://newsapi.org/v2/everything"


def generate_news_id() -> str:
    return f"N-{uuid.uuid4().hex[:8].upper()}"


def parse_datetime(value: str):
    if not value:
        return None

    # NewsAPI format: 2026-05-13T12:00:00Z
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def detect_related_tags(title: str, description: str | None) -> list[str]:
    text = f"{title} {description or ''}".lower()

    tags = []

    keywords = [
        "fashion", "ecommerce", "retail", "clothing",
        "trend", "oversize", "streetwear", "linen",
        "summer", "marketplace", "online shopping"
    ]

    for keyword in keywords:
        if keyword in text:
            tags.append(keyword)

    return tags


def detect_impact_level(tags: list[str]) -> str:
    high_value_tags = {"trend", "fashion", "marketplace"}

    if any(tag in high_value_tags for tag in tags):
        return "high"

    return "medium"


def build_recommended_action(tags: list[str]) -> str:
    if "oversize" in tags or "streetwear" in tags:
        return "Oversize ve streetwear ürünlerinin stok ve reklam performansını kontrol edin."

    if "linen" in tags or "summer" in tags:
        return "Yazlık ve keten ürünlerin stok durumunu gözden geçirin."

    if "ecommerce" in tags or "marketplace" in tags:
        return "Pazaryeri satış performansınızı ve fiyat rekabetinizi kontrol edin."

    return "Bu gelişmenin ürün kategorilerinizle ilişkisini kontrol edin."


def fetch_and_store_market_news(db: Session):
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY bulunamadı. .env dosyasını kontrol et.")

    queries = [
        "fashion ecommerce",
        "retail fashion trends",
        "online marketplace sellers",
        "clothing retail trend",
        "streetwear trend",
        "linen fashion"
    ]

    created_news = 0
    updated_news = 0

    for query in queries:
        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 5,
            "apiKey": NEWS_API_KEY
        }

        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        articles = data.get("articles", [])

        for article in articles:
            title = article.get("title")
            url = article.get("url")

            if not title or not url:
                continue

            source = article.get("source", {}).get("name")
            description = article.get("description")
            published_at = parse_datetime(article.get("publishedAt"))

            related_tags = detect_related_tags(title, description)
            impact_level = detect_impact_level(related_tags)
            recommended_action = build_recommended_action(related_tags)

            existing_news = db.query(MarketNews).filter(
                MarketNews.url == url
            ).first()

            if existing_news:
                existing_news.title = title
                existing_news.original_title = title
                existing_news.summary = description
                existing_news.source = source
                existing_news.published_at = published_at
                existing_news.language = "en"
                existing_news.category = "Market Intelligence"
                existing_news.related_tags = related_tags
                existing_news.impact_level = impact_level
                existing_news.recommended_action = recommended_action
                updated_news += 1

            else:
                news = MarketNews(
                    news_id=generate_news_id(),
                    title=title,
                    original_title=title,
                    summary=description,
                    source=source,
                    url=url,
                    published_at=published_at,
                    language="en",
                    category="Market Intelligence",
                    related_tags=related_tags,
                    impact_level=impact_level,
                    recommended_action=recommended_action
                )

                db.add(news)
                created_news += 1

    db.commit()

    return {
        "message": "NewsAPI haberleri başarıyla çekildi ve kaydedildi.",
        "created_news": created_news,
        "updated_news": updated_news
    }