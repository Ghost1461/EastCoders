import json
import uuid
from pathlib import Path
from sqlalchemy.orm import Session

from app.models import Product, ProductListing


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "mock_sources" / "hepsiburada_product.json"


def generate_product_id() -> str:
    return f"P-{uuid.uuid4().hex[:8].upper()}"


def generate_listing_id() -> str:
    return f"L-{uuid.uuid4().hex[:8].upper()}"


def build_tags(item: dict) -> list[str]:
    tags = []

    for key in ["product_name", "brand", "category_name", "color", "size"]:
        value = item.get(key)
        if value:
            tags.extend(str(value).lower().split())

    return list(set(tags))


def import_hepsiburada_products(db: Session):
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        raw_products = json.load(file)

    imported_products = 0
    created_listings = 0
    updated_listings = 0

    for item in raw_products:
        sku = item["merchant_sku"]

        product = db.query(Product).filter(
            Product.seller_sku == sku
        ).first()

        if not product:
            product = Product(
                internal_product_id=generate_product_id(),
                seller_sku=sku,
                name=item["product_name"],
                brand=item.get("brand"),
                category=item.get("category_name"),
                color=item.get("color"),
                size=item.get("size"),
                tags=build_tags(item)
            )

            db.add(product)
            db.flush()
            imported_products += 1

        listing = db.query(ProductListing).filter(
            ProductListing.platform == "Hepsiburada",
            ProductListing.external_product_id == item["hb_product_id"]
        ).first()

        if listing:
            listing.price = item["sale_price"]
            listing.stock = item["available_stock"]
            listing.commission_rate = item.get("commission_rate")
            listing.rating = item.get("rating")
            listing.review_count = item.get("review_count", 0)
            listing.status = item.get("status", "active")
            updated_listings += 1

        else:
            listing = ProductListing(
                listing_id=generate_listing_id(),
                internal_product_id=product.internal_product_id,
                platform="Hepsiburada",
                external_product_id=item["hb_product_id"],
                seller_sku=sku,
                price=item["sale_price"],
                stock=item["available_stock"],
                commission_rate=item.get("commission_rate"),
                rating=item.get("rating"),
                review_count=item.get("review_count", 0),
                status=item.get("status", "active")
            )

            db.add(listing)
            created_listings += 1

    db.commit()

    return {
        "message": "Hepsiburada products imported successfully",
        "new_products": imported_products,
        "created_listings": created_listings,
        "updated_listings": updated_listings
    }