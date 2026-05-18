from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User

from app.services.review_import_service import import_reviews_service

from app.services.api_service_key import get_source_user_id_from_api_key


router = APIRouter(
    prefix="/reviews",
    tags=["Review_Import"]
)


@router.post("source_user_id/{platform_key}/import_review/{source_user_id}")
def import_reviews_by_platform(
    platform_key: str,
    source_user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    supported_platforms = [
        "amazon",
        "trendyol",
        "hepsiburada"
    ]

    platform_key = platform_key.lower()

    if platform_key not in supported_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Desteklenmeyen platform: {platform_key}"
        )

    return import_reviews_service(
        platform_key=platform_key,
        source_user_id=source_user_id,
        db=db,
        current_user=current_user
    )



@router.post("api_key/{platform_key}/import_review/by-api-key")
def import_reviews_by_api_key(
    platform_key: str,
    api_key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    supported_platforms = [
        "amazon",
        "trendyol",
        "hepsiburada"
    ]

    platform_key = platform_key.lower()

    if platform_key not in supported_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Desteklenmeyen platform: {platform_key}"
        )

    source_user_id = get_source_user_id_from_api_key(
        platform_key=platform_key,
        api_key=api_key
    )

    return import_reviews_service(
        platform_key=platform_key,
        source_user_id=source_user_id,
        db=db,
        current_user=current_user
    )