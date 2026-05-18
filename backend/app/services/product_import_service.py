import json
import uuid
from pathlib import Path
from sqlalchemy.orm import Session
from rapidfuzz import fuzz

from app.models import Product, ProductListing
from app.services.product_normalizer_service import normalize_product
from app.services.connected_account_service import validate_connected_account



BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

PRODUCT_FILES = {
    "hepsiburada": DATA_DIR / "mock_sources" / "hepsiburada_products.json",
    "trendyol": DATA_DIR / "mock_sources" / "trendyol_products.json",
    "amazon": DATA_DIR / "mock_sources" / "amazon_products.json",
}


def find_similar_product(db: Session, item: dict, threshold: int = 90):
    candidates = db.query(Product).filter(
        Product.brand == item.get("brand"),
        Product.category == item.get("category"),
        Product.color == item.get("color"),
        Product.size == item.get("size"),
        Product.gender == item.get("gender"),
    ).all()

    for product in candidates:
        score = fuzz.token_sort_ratio(
            (product.name or "").lower().strip(),
            (item.get("name") or "").lower().strip()
        )

        if score >= threshold:
            return product

    return None


def create_unique_listing_id(db: Session) -> str:
    while True:
        listing_id = f"L-{uuid.uuid4().hex[:8].upper()}"

        exists = db.query(ProductListing).filter(
            ProductListing.listing_id == listing_id
        ).first()

        if not exists:
            return listing_id

#Değişiklik yoksa updated listing'e ekleme
def has_changes(obj, values: dict) -> bool:
    return any(getattr(obj, key) != value for key, value in values.items())


def build_tags(item: dict) -> list[str]:
    tags = []

    for key in ["name", "brand", "category", "color", "size", "gender"]:
        value = item.get(key)
        if value:
            tags.extend(str(value).lower().split())

    return list(set(tags))


def import_products_by_platform(db, platform_key, current_user, source_user_id):
    file_path = PRODUCT_FILES.get(platform_key)

    if not file_path:
        raise ValueError(f"Desteklenmeyen platform: {platform_key}")

    with open(file_path, "r", encoding="utf-8") as file:
        raw_products = json.load(file)

    #Sadece o login olan kullanıcının orderlarını import et(connected account bağlansa bile yanlış seller’ın orderı import edilmez)
    validate_connected_account(
        db=db,
        current_user=current_user,
        platform=platform_key,
        source_user_id=source_user_id
        )
    
    imported_products = 0
    created_listings = 0
    updated_listings = 0

    for raw_item in raw_products:
        item = normalize_product(platform_key, raw_item)

        #connected account bağlansa bile yanlış seller’ın orderı import edilmez
        if str(item.get("source_user_id")) != str(source_user_id):
            continue

        seller_sku = item.get("seller_sku")

        product = db.query(Product).filter(
            Product.name == item.get("name"),
            Product.brand == item.get("brand"),
            Product.category == item.get("category"),
            Product.color == item.get("color"),
            Product.size == item.get("size"),
            Product.gender == item.get("gender"),
        ).first()
        
        if not product:
            product = find_similar_product(db, item)

        if not product:
            product = Product(
                name=item.get("name"),
                brand=item.get("brand"),
                category=item.get("category"),
                gender=item.get("gender"),
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
            product.tags = item.get("tags") or build_tags(item)
            #daha önceden image_url yoksa güncelle, yoksa ezme
            if not product.image_url:
                product.image_url = item.get("image_url")
            product.last_updated = item.get("last_updated")

        listing = db.query(ProductListing).filter(
            ProductListing.user_id == current_user.id,
            ProductListing.external_product_id == item.get("external_product_id"),
            ProductListing.platform == item.get("platform"),
            ProductListing.source_user_id == source_user_id,    
        ).first()

        if listing:
            listing_values = {
                    "seller_sku": seller_sku,
                    "price": item.get("price", 0),
                    "stock": item.get("stock", 0),
                    "commission_rate": item.get("commission_rate"),
                    "rating": item.get("rating"),
                    "review_count": item.get("review_count", 0),
                    "status": item.get("status", "active"),
                }

            if has_changes(listing, listing_values):
                for key, value in listing_values.items():
                    setattr(listing, key, value)
                updated_listings += 1

        else:
            listing = ProductListing(
                listing_id=create_unique_listing_id(db),
                user_id=current_user.id,
                source_user_id=item.get("source_user_id"),#raw datada ismi bu
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


