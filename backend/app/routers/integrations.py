import json
import time
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user_model import User

from app.core.database import get_db
from app.services.product_import_service import (
    import_products_by_platform,
)

router = APIRouter(
    prefix="/integrations",
    tags=["Integrations"]
)


@router.post("/{platform_key}/import-products/{source_user_id}")
def import_platform_products(
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
            detail=f"Unsupported platform: {platform_key}"
        )
    
    return import_products_by_platform(
        db=db,
        platform_key=platform_key,
        user_id=current_user.id,
        source_user_id=source_user_id
    )

def get_source_user_id_from_api_key(platform_key: str, api_key: str) -> str:
    api_keys_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "mock_sources"
        / "api_keys.json"
    )

    with open(api_keys_path, "r", encoding="utf-8") as f:
        api_keys = json.load(f)

    for item in api_keys:
        if (
            item.get("platform", "").lower() == platform_key.lower()
            and item.get("api_key") == api_key
        ):
            return item["user_id"]

    raise HTTPException(
        status_code=401,
        detail="Geçersiz API key veya platform"
    )

@router.post("/{platform_key}/sync-all/by-api-key")
def sync_all_with_api_key(
    platform_key: str,
    api_key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    source_user_id = get_source_user_id_from_api_key(
        platform_key=platform_key,
        api_key=api_key
    )

    product_result = import_products_by_platform(
        db=db,
        platform_key=platform_key,
        user_id=current_user.id,
        source_user_id=source_user_id
    )

    return {
        "message": f"{platform_key} product sync tamamlandı. Order ve review import servisleri henüz eklenmedi.",
        "platform": platform_key,
        "products": product_result,
        "orders": None,
        "reviews": None
    }  
  
# @router.post("/{platform_key}/sync-all/by-api-key")
# def sync_all_with_api_key(
#     platform_key: str,
#     api_key: str,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     source_user_id = get_source_user_id_from_api_key(
#         platform_key=platform_key,
#         api_key=api_key
#     )

#     product_result = import_products_by_platform(
#         db=db,
#         platform_key=platform_key,
#         user_id=current_user.id,
#         source_user_id=source_user_id
#     )

#     time.sleep(3)

#     order_result = import_orders_by_platform(
#         db=db,
#         platform_key=platform_key,
#         user_id=current_user.id,
#         source_user_id=source_user_id
#     )

#     time.sleep(3)

#     review_result = import_reviews_by_platform(
#         db=db,
#         platform_key=platform_key,
#         user_id=current_user.id,
#         source_user_id=source_user_id
#     )

#     return {
#         "message": f"{platform_key} senkronizasyonu tamamlandı",
#         "platform": platform_key,
#         "products": product_result,
#         "orders": order_result,
#         "reviews": review_result
#     }    