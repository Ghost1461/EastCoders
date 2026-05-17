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
    get_lowest_rated_products,
    get_low_stock_products,
    get_user_product_tags,
    get_category_item_counts,
    get_user_product_genders,
    get_gender_distribution,
    get_gender_item_counts,
    get_low_stock_products_by_gender,
)

router = APIRouter(prefix="/products_display", tags=["Products_Display"])




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
    size: str | None = None,
    status: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_stock: int | None = None,
    max_stock: int | None = None,
    min_commission_rate: float | None = None,
    max_commission_rate: float | None = None,
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
        size=size,
        status=status,
        min_price=min_price,
        max_price=max_price,
        min_stock=min_stock,
        max_stock=max_stock,
        min_commission_rate=min_commission_rate,
        max_commission_rate=max_commission_rate,
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

#Productların taglarını getir
@router.get("/options/tags")
def get_tags(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_product_tags(db, current_user.id)

#Cinsiyetleri getir
@router.get("/options/genders")
def get_genders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_product_genders(db, current_user.id)

#Renkleri getir
@router.get("/options/colors")
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

#En az rating yüksek ürünler
@router.get("/ranking/lowest-rated")
def lowest_rated_products(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_lowest_rated_products(db, current_user.id, limit)

#En az yorum alan ürünler
@router.get("/ranking/least-reviewed")
def least_reviewed_products(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_least_reviewed_products(db, current_user.id, limit)


#Stok az olan ürünleri döndür
@router.get("/stock/low")
def low_stock_products(
    threshold: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_low_stock_products(db, current_user.id, threshold)


@router.get("/analytics/category-counts")
def category_item_counts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_category_item_counts(
        db=db,
        user_id=current_user.id
    )


@router.get("/analytics/gender-distribution")
def gender_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_gender_distribution(
        db=db,
        user_id=current_user.id
    )


@router.get("/analytics/gender-item-counts")
def gender_item_counts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_gender_item_counts(
        db=db,
        user_id=current_user.id
    )


@router.get("/low-stock/gender/{gender}")
def low_stock_products_by_gender(
    gender: str,
    threshold: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_low_stock_products_by_gender(
        db=db,
        user_id=current_user.id,
        gender=gender,
        threshold=threshold
    )