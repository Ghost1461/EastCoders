from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.user_model import User
from pydantic import BaseModel
from typing import List
from datetime import date
from app.services.api_service_key import get_source_user_id_from_api_key
from app.services.order_import_service import (
    import_orders_service
)

router = APIRouter(
    prefix="/orders",
    tags=["Order_Import"]
)

#JSON validate için, Swagger docs üretmek için 
class OrderItemImport(BaseModel):
    listing_id: str
    external_product_id: str
    quantity: int
    unit_price: float


class OrderImport(BaseModel):
    order_id: str
    source_user_id: str
    platform: str
    external_order_id: str
    customer_id: str
    items: List[OrderItemImport]
    status: str
    order_date: date



@router.post("source_user_id/{platform_key}/import_order/{source_user_id}")
def import_orders_by_platform(
    platform_key: str,
    source_user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    SUPPORTED_PLATFORMS = [
        "amazon",
        "trendyol",
        "hepsiburada",
    ]

    if platform_key.lower() not in SUPPORTED_PLATFORMS:
        raise HTTPException(
            status_code=400,
            detail=f"Desteklenmeyen platform: {platform_key}"
        )
    
    return import_orders_service(
        platform_key=platform_key.lower(),
        source_user_id=source_user_id,
        db=db,
        current_user=current_user
    )




@router.post("api_key/{platform_key}/import_order/by-api-key")
def import_orders_by_api_key(
    platform_key: str,
    api_key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    SUPPORTED_PLATFORMS = [
        "amazon",
        "trendyol",
        "hepsiburada",
    ]

    platform_key = platform_key.lower()

    if platform_key not in SUPPORTED_PLATFORMS:
        raise HTTPException(
            status_code=400,
            detail=f"Desteklenmeyen platform: {platform_key}"
        )

    source_user_id = get_source_user_id_from_api_key(
        platform_key=platform_key,
        api_key=api_key
    )

    return import_orders_service(
        platform_key=platform_key,
        source_user_id=source_user_id,
        db=db,
        current_user=current_user
    )