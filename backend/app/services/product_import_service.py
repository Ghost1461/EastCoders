import json
import uuid
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Product, ProductListing
from app.services.product_normalizer_service import normalize_product


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

PRODUCT_FILES = {
    "hepsiburada": DATA_DIR / "mock_sources" / "hepsiburada_products.json",
    "trendyol": DATA_DIR / "mock_sources" / "trendyol_products.json",
    "amazon": DATA_DIR / "mock_sources" / "amazon_products.json",
}




def create_unique_listing_id(db: Session) -> str:
    while True:
        listing_id = f"L-{uuid.uuid4().hex[:8].upper()}"

        exists = db.query(ProductListing).filter(
            ProductListing.listing_id == listing_id
        ).first()

        if not exists:
            return listing_id


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

        seller_sku = item.get("seller_sku")

        product = db.query(Product).filter(
            Product.name == item.get("name"),
            Product.brand == item.get("brand"),
            Product.category == item.get("category"),
            Product.color == item.get("color"),
            Product.size == item.get("size"),
        ).first()

        if not product:
            product = Product(
                name=item.get("name"),
                brand=item.get("brand"),
                category=item.get("category"),
                color=item.get("color"),
                size=item.get("size"),
                tags=item.get("tags") or build_tags(item),
                image_url=item.get("image_url"),
                last_updated=item.get("last_updated"),
            )

            db.add(product)
            db.flush()
            imported_products += 1
        else:
            product.name = item.get("name", product.name)
            product.brand = item.get("brand")
            product.category = item.get("category")
            product.color = item.get("color")
            product.size = item.get("size")
            product.tags = item.get("tags") or build_tags(item)
            product.image_url = item.get("image_url")
            product.last_updated = item.get("last_updated")

        listing = db.query(ProductListing).filter(
            ProductListing.platform == item.get("platform"),
            ProductListing.external_product_id == item.get("external_product_id"),
        ).first()

        if listing:
            listing.seller_sku = seller_sku
            listing.price = item.get("price", 0)
            listing.stock = item.get("stock", 0)
            listing.commission_rate = item.get("commission_rate")
            listing.rating = item.get("rating")
            listing.review_count = item.get("review_count", 0)
            listing.status = item.get("status", "active")
            updated_listings += 1

        else:
            listing = ProductListing(
                listing_id=create_unique_listing_id(db),
                internal_product_id=product.id,
                platform=item.get("platform"),
                external_product_id=item.get("external_product_id"),
                seller_sku=seller_sku,
                price=item.get("price", 0),
                stock=item.get("stock", 0),
                commission_rate=item.get("commission_rate"),
                rating=item.get("rating"),
                review_count=item.get("review_count", 0),
                status=item.get("status", "active"),
            )

            db.add(listing)
            created_listings += 1

    db.commit()

    return {
        "platform": platform_key,
        "message": f"{platform_key} ürünleri başarıyla aktarıldı",
        "new_products": imported_products,
        "created_listings": created_listings,
        "updated_listings": updated_listings,
    }


def import_all_products(db: Session):
    results = []

    for platform_key in PRODUCT_FILES.keys():
        result = import_products_by_platform(db, platform_key)
        results.append(result)

    return {
        "message": "Tüm platform ürünleri başarıyla aktarıldı",
        "results": results,
    }