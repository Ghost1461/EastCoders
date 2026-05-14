from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Product, ProductListing, User
from app.core.security import get_current_user

router = APIRouter(prefix="/products_import", tags=["Import"])


#belki lazım olabilir, product temelli nested response dönüyor
@router.get("/display_all_products")
def get_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    products = db.query(Product).all()

    result = []

    for product in products:
        listings = db.query(ProductListing).filter(
            ProductListing.internal_product_id == product.id,
            ProductListing.user_id == current_user.id
        ).all()

        if not listings:
            continue

        result.append({
            "internal_product_id": product.id,
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
