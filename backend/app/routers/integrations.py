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


