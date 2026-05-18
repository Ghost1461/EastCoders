from datetime import datetime

from sqlalchemy.orm import Session

from app.models.trend_model import Trend
from app.models.product_model import Product
from app.models.product_listing_model import ProductListing

from app.services.trendyol_trend_scraper_service import fetch_trendyol_best_sellers
from app.services.trend_normalizer_service import normalize_product_name

from app.services.trend_score_service import (
    calculate_trend_score,
    calculate_marketplace_rank_signal,
    calculate_keyword_strength
)


MARKET_SCRAPE_LIMIT = 40
TREND_DISPLAY_LIMIT = 20


async def generate_market_trends_for_system(db: Session):
    scraped_products = await fetch_trendyol_best_sellers(limit=MARKET_SCRAPE_LIMIT)

    created = 0
    updated = 0

    for item in scraped_products:
        trend_key = item["trend_key"]

        rank_signal = calculate_marketplace_rank_signal(
            rank=item.get("rank"),
            max_rank=MARKET_SCRAPE_LIMIT
        )
        keyword_strength = calculate_keyword_strength(trend_key=trend_key)
        social_signal = item.get("social_signal", 0)

        rating_signal = 0
        if item.get("rating"):
            rating_signal = round(item["rating"] / 5, 2)

        score = calculate_trend_score(
            marketplace_signal=rank_signal,
            sales_growth=social_signal,
            review_growth=0,
            rating_signal=rating_signal,
            stock_signal=0,
            news_signal=0,
            keyword_strength=keyword_strength
        )

        extra_data = {
            "rank": item.get("rank"),
            "brand": item.get("brand"),
            "price_text": item.get("price_text"),
            "price": item.get("price"),
            "rating_text": item.get("rating_text"),
            "rating": item.get("rating"),
            "review_count_text": item.get("review_count_text"),
            "review_count": item.get("review_count"),
            "order_count_text": item.get("order_count_text"),
            "order_count": item.get("order_count"),
            "favorite_count_text": item.get("favorite_count_text"),
            "favorite_count": item.get("favorite_count"),
            "view_count_text": item.get("view_count_text"),
            "view_count": item.get("view_count"),
            "social_signal": social_signal,
            "rank_signal": rank_signal,
            "keyword_strength": keyword_strength
        }

        existing = (
            db.query(Trend)
            .filter(
                Trend.trend_key == trend_key,
                Trend.source == item["source"]
            )
            .first()
        )

        if existing:
            existing.trend_name = item["trend_name"]
            existing.category = item.get("category")
            existing.platform = item.get("platform")
            existing.marketplace_signal = rank_signal
            existing.sales_growth = social_signal
            existing.review_growth = 0
            existing.rating_signal = rating_signal
            existing.stock_signal = 0
            existing.news_signal = 0
            existing.trend_score = score
            existing.image_url = item.get("image_url")
            existing.extra_data = extra_data
            existing.explanation = f"{item['trend_name']} Trendyol çok satanlarda görünüyor."
            existing.updated_at = datetime.utcnow()
            updated += 1
        else:
            trend = Trend(
                trend_key=trend_key,
                trend_name=item["trend_name"],
                trend_type="market_trend",
                source=item["source"],
                category=item.get("category"),
                platform=item.get("platform"),
                marketplace_signal=rank_signal,
                sales_growth=social_signal,
                review_growth=0,
                rating_signal=rating_signal,
                stock_signal=0,
                news_signal=0,
                trend_score=score,
                image_url=item.get("image_url"),
                extra_data=extra_data,
                explanation=f"{item['trend_name']} Trendyol çok satanlarda görünüyor."
            )

            db.add(trend)
            created += 1

    db.commit()

    return {
        "message": "Market trendleri üretildi.",
        "scraped": len(scraped_products),
        "created": created,
        "updated": updated
    }


CATEGORY_TRANSLATION_MAP = {
    "kapüşonlu": "kapusonlu",
    "kapusonlu": "kapusonlu",
    "hoodie": "kapusonlu",
    "sweatshirt": "kapusonlu",

    "t-shirt": "tshirt",
    "tshirt": "tshirt",
    "tişört": "tshirt",
    "tisort": "tshirt",
    "shirt": "tshirt",

    "pantolon": "pantolon",
    "pants": "pantolon",
    "trouser": "pantolon",
    "trousers": "pantolon",

    "şapka": "sapka",
    "sapka": "sapka",
    "hat": "sapka",

    "elbise": "elbise",
    "dress": "elbise",

    "ceket": "ceket",
    "jacket": "ceket",

    "çorap": "corap",
    "corap": "corap",
    "sock": "corap",
    "socks": "corap"
}


PRODUCT_TYPE_WORDS = {
    "kapusonlu",
    "tshirt",
    "pantolon",
    "sapka",
    "elbise",
    "ceket",
    "corap"
}


MATCH_STOPWORDS = {
    "basic",
    "unisex",
    "kadin",
    "kadın",
    "erkek",
    "cocuk",
    "çocuk",
    "pamuklu",
    "siyah",
    "beyaz",
    "bej",
    "mavi",
    "pembe",
    "pink",
    "yellow",
    "purple",
    "black",
    "white",
    "fashion",
    "moda",
    "adet",
    "cift",
    "çift",
    "lu",
    "li",
    "lı",
    "8"
}


def normalize_for_match(text: str):
    text = normalize_product_name(text or "")

    words = text.split()
    translated_words = []

    for word in words:
        translated_words.append(
            CATEGORY_TRANSLATION_MAP.get(word, word)
        )

    return " ".join(translated_words)


def find_user_matching_listings(
    db: Session,
    trend_key: str
):
    listings = (
        db.query(ProductListing)
        .join(Product)
        .all()
    )

    matched = []

    normalized_trend_key = normalize_for_match(trend_key)

    trend_words = {
        word for word in normalized_trend_key.split()
        if word not in MATCH_STOPWORDS and len(word) > 2
    }

    trend_product_types = trend_words.intersection(PRODUCT_TYPE_WORDS)

    if not trend_product_types:
        return matched

    for listing in listings:
        product_name = listing.product.name or ""
        product_category = listing.product.category or ""

        normalized_product_name = normalize_for_match(product_name)
        normalized_product_category = normalize_for_match(product_category)

        product_words = {
            word for word in (
                normalized_product_name.split()
                + normalized_product_category.split()
            )
            if word not in MATCH_STOPWORDS and len(word) > 2
        }

        product_types = product_words.intersection(PRODUCT_TYPE_WORDS)
        common_product_types = trend_product_types.intersection(product_types)

        if common_product_types:
            matched.append(listing.listing_id)

    return matched


def serialize_market_trend(trend: Trend):
    return {
        "id": trend.id,
        "trend_key": trend.trend_key,
        "trend_name": trend.trend_name,
        "trend_type": trend.trend_type,
        "source": trend.source,
        "category": trend.category,
        "platform": trend.platform,
        "marketplace_signal": trend.marketplace_signal,
        "sales_growth": trend.sales_growth,
        "review_growth": trend.review_growth,
        "rating_signal": trend.rating_signal,
        "stock_signal": trend.stock_signal,
        "news_signal": trend.news_signal,
        "trend_score": trend.trend_score,
        "image_url": trend.image_url,
        "extra_data": trend.extra_data,
        "explanation": trend.explanation,
        "created_at": trend.created_at,
        "updated_at": trend.updated_at
    }


def attach_personalization_to_trends(
    db: Session,
    trends
):
    result = []

    for trend in trends:
        matched_listing_ids = find_user_matching_listings(
            db=db,
            trend_key=trend.trend_key
        )

        item = serialize_market_trend(trend)
        item["is_personalized"] = bool(matched_listing_ids)
        item["matched_listing_ids"] = matched_listing_ids

        result.append(item)

    return result


def get_raw_trends(
    db: Session,
    limit: int = 40
):
    trends = (
        db.query(Trend)
        .filter(Trend.trend_type == "market_trend")
        .all()
    )

    result = []

    for trend in trends:
        result.append({
            "id": trend.id,
            "trend_name": trend.trend_name,
            "source": trend.source,
            "category": trend.category,
            "platform": trend.platform,
            "image_url": trend.image_url,
            "extra_data": trend.extra_data,
            "created_at": trend.created_at,
            "updated_at": trend.updated_at
        })

    result.sort(
        key=lambda item: (item.get("extra_data") or {}).get("rank", 999)
    )

    return result[:limit]


def get_market_trends(
    db: Session,
    limit: int = TREND_DISPLAY_LIMIT
):
    trends = (
        db.query(Trend)
        .filter(Trend.trend_type == "market_trend")
        .order_by(Trend.trend_score.desc())
        .limit(limit)
        .all()
    )

    return [
        serialize_market_trend(trend)
        for trend in trends
    ]

def get_matched_products_for_trend(
    db: Session,
    trend_key: str
):
    listings = (
        db.query(ProductListing)
        .join(Product)
        .all()
    )

    matched_products = []

    normalized_trend_key = normalize_for_match(trend_key)

    trend_words = {
        word for word in normalized_trend_key.split()
        if word not in MATCH_STOPWORDS and len(word) > 2
    }

    trend_product_types = trend_words.intersection(PRODUCT_TYPE_WORDS)

    if not trend_product_types:
        return matched_products

    for listing in listings:
        product = listing.product

        product_name = product.name or ""
        product_category = product.category or ""

        normalized_product_name = normalize_for_match(product_name)
        normalized_product_category = normalize_for_match(product_category)

        product_words = {
            word for word in (
                normalized_product_name.split()
                + normalized_product_category.split()
            )
            if word not in MATCH_STOPWORDS and len(word) > 2
        }

        product_types = product_words.intersection(PRODUCT_TYPE_WORDS)
        common_product_types = trend_product_types.intersection(product_types)

        if common_product_types:
            matched_products.append({
                "listing_id": listing.listing_id,
                "product_id": product.id,
                "product_name": product.name,

                "brand": product.brand,
                "category": product.category,
                "color": product.color,
                "size": product.size,

                "platform": listing.platform,
                "seller_sku": listing.seller_sku,

                "price": listing.price,
                "stock": listing.stock,
                "rating": listing.rating,
                "review_count": listing.review_count,
                "status": listing.status
            })

    return matched_products

def get_personalized_market_trends(
    db: Session,
    limit: int = TREND_DISPLAY_LIMIT
):
    trends = (
        db.query(Trend)
        .filter(Trend.trend_type == "market_trend")
        .order_by(Trend.trend_score.desc())
        .all()
    )

    result = []

    for trend in trends:
        matched_products = get_matched_products_for_trend(
            db=db,
            trend_key=trend.trend_key
        )

        if not matched_products:
            continue

        result.append({
            "trend": serialize_market_trend(trend),
            "matched_products": matched_products
        })

    return result[:limit]

def get_all_trends(
    db: Session,
    limit: int = TREND_DISPLAY_LIMIT
):
    trends = (
        db.query(Trend)
        .order_by(Trend.trend_score.desc())
        .limit(limit)
        .all()
    )

    return [
        serialize_market_trend(trend)
        for trend in trends
    ]