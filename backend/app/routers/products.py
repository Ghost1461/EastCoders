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

@router.get("/return_pro")
def get_products():
    return [
        {"id": 1, "name": "Sweatshirt"},
        {"id": 2, "name": "Skirt"}
    ]


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
            "seller_sku": product.seller_sku,
            "name": product.name,
            "brand": product.brand,
            "category": product.category,
            "color": product.color,
            "size": product.size,
            "tags": product.tags,
            "listings": [
                {
                    "listing_id": listing.listing_id,
                    "platform": listing.platform,
                    "external_product_id": listing.external_product_id,
                    "price": listing.price,
                    "stock": listing.stock,
                    "rating": listing.rating,
                    "review_count": listing.review_count,
                    "status": listing.status
                }
                for listing in listings
            ]
        })

    return result