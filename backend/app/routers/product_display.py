#frontende product verisi dönmek için
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import User
from app.core.security import get_current_user
from app.services.product_display_service import (
    get_all_user_products,
    get_user_products_by_platform,
    get_product_detail,
    search_user_products,
    filter_user_products,
    get_user_product_categories,
    get_user_product_brands,
    get_user_product_colors,
    get_most_reviewed_products,
    get_top_rated_products,
    get_least_reviewed_products,
    get_lowest_rated_products
)

router = APIRouter(prefix="/products_display", tags=["Products","Display"])




#Kullanıcı tüm listelediği ürünleri getirir
@router.get("/all")
def display_all_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_user_products(db, current_user.id)



#Platforma göre ürünleri getir
@router.get("/platform/{platform_key}")
def display_products_by_platform(
    platform_key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_products_by_platform(db, current_user.id, platform_key)


#Listelenen ürünün tek tek ürün detayı
@router.get("/detail/{listing_id}")
def display_product_detail(
    listing_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_product_detail(db, current_user.id, listing_id)



#Name'e göre arama yapmak için kendi ürünleri arasında
@router.get("/search/name")
def search_products_by_name(
    q: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return search_user_products(db, current_user.id, q)



#Filtreleme yapmak için
@router.get("/filter")
def filter_products(
    platform: str | None = None,
    brand: str | None = None,
    category: str | None = None,
    color: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return filter_user_products(
        db=db,
        user_id=current_user.id,
        platform=platform,
        brand=brand,
        category=category,
        color=color,
        min_price=min_price,
        max_price=max_price,
    )




#Kategorileri getir
@router.get("/options/categories")
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_product_categories(db, current_user.id)

#Markaları getir
@router.get("/options/brands")
def get_brands(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_product_brands(db, current_user.id)


#Renkleri getir
def get_colors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_product_colors(db, current_user.id)


#En çok yorum alan ürünler
@router.get("/ranking/most-reviewed")
def most_reviewed_products(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_most_reviewed_products(db, current_user.id, limit)



#En çok rating yüksek ürünler
@router.get("/ranking/top-rated")
def top_rated_products(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_top_rated_products(db, current_user.id, limit)


@router.get("/ranking/lowest-rated")
def lowest_rated_products(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_lowest_rated_products(db, current_user.id, limit)


@router.get("/ranking/least-reviewed")
def least_reviewed_products(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_least_reviewed_products(db, current_user.id, limit)


#Stok az olan ürünler(sorna ekle, o order.jsonlarda)
#@router.get("/platform/{platform_key}")
