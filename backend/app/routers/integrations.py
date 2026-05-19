import json
import time
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user_model import User

from app.services.api_service_key import (
    get_source_user_id_from_api_key
)

from app.core.database import get_db
from app.services.product_import_service import (
    import_products_by_platform,
)

router = APIRouter(
    prefix="/integrations",
    tags=["Integrations"]
)


@router.post("source_user_id/{platform_key}/import-products/{source_user_id}")
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
            detail=f"Desteklenmeyen platform: {platform_key}"
        )
    
    return import_products_by_platform(
        db=db,
        platform_key=platform_key.lower(),
        current_user=current_user,
        source_user_id=source_user_id
    )

# API key ile product import yapar
# API key -> source_user_id dönüşümü backend içinde yapılır
@router.post("api_key/{platform_key}/import-products/by-api-key")
def import_platform_products_by_api_key(
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

    return import_products_by_platform(
        db=db,
        platform_key=platform_key,
        current_user=current_user,
        source_user_id=source_user_id
    )