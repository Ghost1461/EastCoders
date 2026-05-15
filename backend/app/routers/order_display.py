from typing import Optional
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User

from app.services.order_display_services import (
    get_all_orders_service,
    get_orders_by_platform_service,
    get_orders_by_status_service,
    get_orders_by_date_range_service,
    search_orders_service,
    get_order_detail_service,
    get_order_items_service,
    get_order_summary_service,
    get_daily_order_analysis_service,
    get_weekly_order_analysis_service,
    get_monthly_order_analysis_service,
    get_platform_analysis_service,
)


router = APIRouter(
    prefix="/orders",
    tags=["Order_Display"]
)


################################################################ 1. Order listeleme
# - Mevcut giriş yapmış kullanıcının tüm orderlarını getir
@router.get("/")
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_orders_service(
        db=db,
        current_user=current_user
    )

# - Platforma göre filtrele: amazon, trendyol, hepsiburada
@router.get("/platform/{platform_key}")
def get_orders_by_platform(
    platform_key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_orders_by_platform_service(
        platform_key=platform_key,
        db=db,
        current_user=current_user
    )



# - Status'a göre filtrele: shipped, returned, cancelled, delivered
@router.get("/status/{status}")
def get_orders_by_status(
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_orders_by_status_service(
        status=status,
        db=db,
        current_user=current_user
    )


# - Tarih aralığına göre filtrele: start_date, end_date
@router.get("/date-range")
def get_orders_by_date_range(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_orders_by_date_range_service(
        start_date=start_date,
        end_date=end_date,
        db=db,
        current_user=current_user
    )


# - Order id / external order id ile arama yap
@router.get("/search")
def search_orders(
    q: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return search_orders_service(
        q=q,
        db=db,
        current_user=current_user
    )

################################################################ 2. Order detay(yedek)
# - Seçilen order'ın ana bilgilerini getir
@router.get("/get_order_details/{order_id}")
def get_order_detail(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_order_detail_service(
        order_id=order_id,
        db=db,
        current_user=current_user
    )


# - Order itemlarını getir
@router.get("/get_order_item_details/{order_id}/items")
def get_order_items(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_order_items_service(
        order_id=order_id,
        db=db,
        current_user=current_user
    )

################################################################ 3. Order summary
# - total_orders
# - total_revenue
# - delivered_orders
# - cancelled_orders
# - returned_orders
# - shipped_orders
# - average_order_value
@router.get("/get/summary")
def get_order_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_order_summary_service(
        db=db,
        current_user=current_user
    )

################################################################ 4. Zaman bazlı order analizleri
# - Günlük order bilgileri
@router.get("/analysis/daily")
def get_daily_order_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_daily_order_analysis_service(
        db=db,
        current_user=current_user
    )

# - Haftalık order bilgileri
@router.get("/analysis/weekly")
def get_weekly_order_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_weekly_order_analysis_service(
        db=db,
        current_user=current_user
    )


# - Aylık order bilgileri
@router.get("/analysis/monthly")
def get_monthly_order_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_monthly_order_analysis_service(
        db=db,
        current_user=current_user
    )

################################################################ 5. Platform bazlı analiz
# - Amazon / Trendyol / Hepsiburada bazlı order sayısı ve revenue
@router.get("/analysis/platform")
def get_platform_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_platform_analysis_service(
        db=db,
        current_user=current_user
    )