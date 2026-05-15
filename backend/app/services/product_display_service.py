from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.models import Product, ProductListing

#frontend’e JSON döndürmek için(SQLAlchemy objesini direkt döndürmek sıkıntılı olabilir)
def serialize_product_listing(listing: ProductListing):
    product = listing.product

    return {
        "listing_id": listing.listing_id,
        "user_id": listing.user_id,
        "source_user_id": listing.source_user_id,
        "platform": listing.platform,
        "external_product_id": listing.external_product_id,
        "seller_sku": listing.seller_sku,
        "price": listing.price,
        "stock": listing.stock,
        "commission_rate": listing.commission_rate,
        "rating": listing.rating,
        "review_count": listing.review_count,
        "status": listing.status,

        "product": {
            "id": product.id,
            "name": product.name,
            "brand": product.brand,
            "category": product.category,
            "color": product.color,
            "size": product.size,
            "tags": product.tags,
            "image_url": product.image_url,
            "last_updated": product.last_updated,
        } if product else None
    }


def base_user_products_query(db: Session, user_id: int):
    return (
        db.query(ProductListing)
        .join(Product, ProductListing.internal_product_id == Product.id)
        .filter(ProductListing.user_id == user_id)#Login olan kullanıcının listinglerini hesaba kat sadece
    )


def get_all_user_products(db: Session, user_id: int):
    listings = base_user_products_query(db, user_id).all()

    return {
        "count": len(listings),
        "products": [serialize_product_listing(listing) for listing in listings]
    }


def get_user_products_by_platform(db: Session, user_id: int, platform_key: str):
    listings = (
        base_user_products_query(db, user_id)
        .filter(ProductListing.platform == platform_key)
        .all()
    )

    return {
        "platform": platform_key,
        "count": len(listings),
        "products": [serialize_product_listing(listing) for listing in listings]
    }


def get_product_detail(db: Session, user_id: int, listing_id: str):
    listing = (
        base_user_products_query(db, user_id)
        .filter(ProductListing.listing_id == listing_id)
        .first()
    )

    if not listing:
        return {
            "message": "Ürün bulunamadı",
            "product": None
        }

    return serialize_product_listing(listing)


def search_user_products(db: Session, user_id: int, q: str):
    search_text = f"%{q}%"

    listings = (
        base_user_products_query(db, user_id)
        .filter(Product.name.ilike(search_text))
        .all()
    )

    return {
        "query": q,
        "count": len(listings),
        "products": [serialize_product_listing(listing) for listing in listings]
    }


def filter_user_products(
    db: Session,
    user_id: int,
    platform: str | None = None,
    brand: str | None = None,
    category: str | None = None,
    color: str | None = None,
    size: str | None = None,
    status: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_stock: int | None = None,
    max_stock: int | None = None,
    min_commission_rate: float | None = None,
    max_commission_rate: float | None = None,
):
    query = base_user_products_query(db, user_id)

    if platform:
        query = query.filter(func.lower(ProductListing.platform) == platform.lower())

    if brand:
        query = query.filter(func.lower(Product.brand) == brand.lower())

    if category:
        query = query.filter(func.lower(Product.category) == category.lower())

    if color:
        query = query.filter(func.lower(Product.color) == color.lower())

    if size:
        query = query.filter(func.lower(Product.size) == size.lower())

    if status:
        query = query.filter(func.lower(ProductListing.status) == status.lower())

    if min_price is not None:
        query = query.filter(ProductListing.price >= min_price)

    if max_price is not None:
        query = query.filter(ProductListing.price <= max_price)

    if min_stock is not None:
        query = query.filter(ProductListing.stock >= min_stock)

    if max_stock is not None:
        query = query.filter(ProductListing.stock <= max_stock)

    if min_commission_rate is not None:
        query = query.filter(ProductListing.commission_rate >= min_commission_rate)

    if max_commission_rate is not None:
        query = query.filter(ProductListing.commission_rate <= max_commission_rate)

    listings = query.all()

    return {
        "count": len(listings),
        "filters": {
            "platform": platform,
            "brand": brand,
            "category": category,
            "color": color,
            "size": size,
            "status": status,
            "min_price": min_price,
            "max_price": max_price,
            "min_stock": min_stock,
            "max_stock": max_stock,
            "min_commission_rate": min_commission_rate,
            "max_commission_rate": max_commission_rate,
        },
        "products": [serialize_product_listing(listing) for listing in listings]
    }


def get_user_product_categories(db: Session, user_id: int):
    rows = (
        base_user_products_query(db, user_id)
        .with_entities(Product.category)
        .distinct()
        .all()
    )

    return {
        "categories": [row[0] for row in rows if row[0]]
    }


def get_user_product_brands(db: Session, user_id: int):
    rows = (
        base_user_products_query(db, user_id)
        .with_entities(Product.brand)
        .distinct()
        .all()
    )

    return {
        "brands": [row[0] for row in rows if row[0]]
    }


def get_user_product_colors(db: Session, user_id: int):
    rows = (
        base_user_products_query(db, user_id)
        .with_entities(Product.color)
        .distinct()
        .all()
    )

    return {
        "colors": [row[0] for row in rows if row[0]]
    }


def get_most_reviewed_products(db: Session, user_id: int, limit: int = 10):
    listings = (
        base_user_products_query(db, user_id)
        .order_by(desc(ProductListing.review_count))
        .limit(limit)
        .all()
    )

    return {
        "count": len(listings),
        "products": [serialize_product_listing(listing) for listing in listings]
    }


def get_top_rated_products(db: Session, user_id: int, limit: int = 10):
    listings = (
        base_user_products_query(db, user_id)
        .order_by(desc(ProductListing.rating))
        .limit(limit)
        .all()
    )

    return {
        "count": len(listings),
        "products": [serialize_product_listing(listing) for listing in listings]
    }


def get_lowest_rated_products(db: Session, user_id: int, limit: int = 10):
    listings = (
        base_user_products_query(db, user_id)
        .order_by(ProductListing.rating.asc())
        .limit(limit)
        .all()
    )

    return {
        "count": len(listings),
        "products": [serialize_product_listing(listing) for listing in listings]
    }


def get_least_reviewed_products(db: Session, user_id: int, limit: int = 10):
    listings = (
        base_user_products_query(db, user_id)
        .order_by(ProductListing.review_count.asc())
        .limit(limit)
        .all()
    )

    return {
        "count": len(listings),
        "products": [serialize_product_listing(listing) for listing in listings]
    }


def get_low_stock_products(
    db: Session,
    user_id: int,
    threshold: int = 10
):
    listings = (
        base_user_products_query(db, user_id)
        .filter(ProductListing.stock <= threshold)
        .order_by(ProductListing.stock.asc())
        .all()
    )

    return {
        "threshold": threshold,
        "count": len(listings),
        "products": [serialize_product_listing(listing) for listing in listings]
    }


def get_user_product_tags(
    db: Session,
    user_id: int
):
    listings = base_user_products_query(db, user_id).all()

    tags_set = set()

    for listing in listings:
        product = listing.product

        if product and product.tags:
            for tag in product.tags:
                tags_set.add(tag)

    return {
        "count": len(tags_set),
        "tags": sorted(list(tags_set))
    }


def get_category_item_counts(
    db: Session,
    user_id: int
):
    results = (
        base_user_products_query(db, user_id)
        .with_entities(
            Product.category,
            func.count(Product.id)
        )
        .group_by(Product.category)
        .order_by(func.count(Product.id).desc())
        .all()
    )

    categories = []

    for category, count in results:
        categories.append({
            "category": category,
            "count": count
        })

    return {
        "total_categories": len(categories),
        "categories": categories
    }