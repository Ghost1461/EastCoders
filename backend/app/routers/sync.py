from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User

from app.services.sync_service import sync_platform_service


router = APIRouter(
    prefix="/sync",
    tags=["Sync"]
)


@router.post("/{platform_key}/{source_user_id}")
def sync_platform(
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
            detail=f"Unsupported platform: {platform_key}"
        )

    return sync_platform_service(
        platform_key=platform_key,
        source_user_id=source_user_id,
        db=db,
        current_user=current_user
    )