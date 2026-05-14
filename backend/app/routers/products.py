from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Product, ProductListing
from app.core.database import get_db
from app.models import Product, ProductListing

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def is_ok():
    return {"message": "Products route çalışıyor"}



@router.get("/display_products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    result = []

    for product in products:
        listings = db.query(ProductListing).filter(
            ProductListing.internal_product_id == product.internal_product_id
        ).all()

        result.append({
            "internal_product_id": product.internal_product_id,
            "name": product.name,
            "brand": product.brand,
            "category": product.category,
            "color": product.color,
            "size": product.size,
            "tags": product.tags,
            "image_url": product.image_url,
            "last_updated": product.last_updated,
            "listings": [
                {
                    "listing_id": listing.listing_id,
                    "platform": listing.platform,
                    "external_product_id": listing.external_product_id,
                    "seller_sku": listing.seller_sku,
                    "price": listing.price,
                    "stock": listing.stock,
                    "commission_rate": listing.commission_rate,
                    "rating": listing.rating,
                    "review_count": listing.review_count,
                    "status": listing.status
                }
                for listing in listings
            ]
        })

    return result