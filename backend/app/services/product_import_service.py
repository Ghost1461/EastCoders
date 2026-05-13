import json
import uuid
from pathlib import Path
from sqlalchemy.orm import Session

from app.models import Product, ProductListing
from app.services.product_normalizer_service import normalize_product


BASE_DIR = Path(__file__).resolve().parents[2]

PRODUCT_FILES = {
    "hepsiburada": BASE_DIR / "data" / "mock_sources" / "hepsiburada_product.json",
    "trendyol": BASE_DIR / "data" / "mock_sources" / "trendyol_product.json",
    "amazon": BASE_DIR / "data" / "mock_sources" / "amazon_product.json",
}


def generate_product_id() -> str:
    return f"P-{uuid.uuid4().hex[:8].upper()}"


def generate_listing_id() -> str:
    return f"L-{uuid.uuid4().hex[:8].upper()}"


def build_tags(item: dict) -> list[str]:
    tags = []

    for key in ["name", "brand", "category", "color", "size"]:
        value = item.get(key)
        if value:
            tags.extend(str(value).lower().split())

    return list(set(tags))


def import_products_by_platform(db: Session, platform_key: str):
    file_path = PRODUCT_FILES.get(platform_key)

    if not file_path:
        raise ValueError(f"Unsupported platform: {platform_key}")

    with open(file_path, "r", encoding="utf-8") as file:
        raw_products = json.load(file)

    imported_products = 0
    created_listings = 0
    updated_listings = 0

    for raw_item in raw_products:
        item = normalize_product(platform_key, raw_item)

        sku = item["seller_sku"]

        product = db.query(Product).filter(
            Product.seller_sku == sku
        ).first()

        if not product:
            product = Product(
                internal_product_id=generate_product_id(),
                seller_sku=sku,
                name=item["name"],
                brand=item.get("brand"),
                category=item.get("category"),
                color=item.get("color"),
                size=item.get("size"),
                tags=build_tags(item)
            )

            db.add(product)
            db.flush()
            imported_products += 1

        listing = db.query(ProductListing).filter(
            ProductListing.platform == item["platform"],
            ProductListing.external_product_id == item["external_product_id"]
        ).first()

        if listing:
            listing.price = item["price"]
            listing.stock = item["stock"]
            listing.commission_rate = item.get("commission_rate")
            listing.rating = item.get("rating")
            listing.review_count = item.get("review_count", 0)
            listing.status = item.get("status", "active")
            updated_listings += 1

        else:
            listing = ProductListing(
                listing_id=generate_listing_id(),
                internal_product_id=product.internal_product_id,
                platform=item["platform"],
                external_product_id=item["external_product_id"],
                seller_sku=sku,
                price=item["price"],
                stock=item["stock"],
                commission_rate=item.get("commission_rate"),
                rating=item.get("rating"),
                review_count=item.get("review_count", 0),
                status=item.get("status", "active")
            )

            db.add(listing)
            created_listings += 1

    db.commit()

    return {
        "platform": platform_key,
        "message": f"{platform_key} ürünleri başarıyla aktarıldı",
        "new_products": imported_products,
        "created_listings": created_listings,
        "updated_listings": updated_listings
    }


def import_all_products(db: Session):
    results = []

    for platform_key in PRODUCT_FILES.keys():
        result = import_products_by_platform(db, platform_key)
        results.append(result)

    return {
        "message": "Tüm platform ürünleri başarıyla aktarıldı",
        "results": results
    }