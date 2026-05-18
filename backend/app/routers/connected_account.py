#current_user sadece kendi bağladığı platform + source_user_id hesabından import yapabilsin diye ConnectedAccount yapısı
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User

from app.services.connected_account_service import (
    connect_platform_account_service,
    get_connected_accounts_service,
    deactivate_connected_account_service
)

SUPPORTED_PLATFORMS = [
    "amazon",
    "trendyol",
    "hepsiburada",
]

router = APIRouter(
    prefix="/connected-accounts",
    tags=["Connected_Accounts"]
)


def validate_platform(platform: str) -> str:
    platform = platform.lower()

    if platform not in SUPPORTED_PLATFORMS:
        raise HTTPException(
            status_code=400,
            detail=f"Desteklenmeyen platform: {platform}"
        )

    return platform


@router.post("/{platform}/connect/{source_user_id}")
def connect_platform_account(
    platform: str,
    source_user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    platform = validate_platform(platform)

    return connect_platform_account_service(
        db=db,
        current_user=current_user,
        platform=platform,
        source_user_id=source_user_id
    )


@router.get("/")
def get_connected_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_connected_accounts_service(
        db=db,
        current_user=current_user
    )


@router.put("/{platform}/deactivate/{source_user_id}")
def deactivate_connected_account(
    platform: str,
    source_user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    platform = validate_platform(platform)

    return deactivate_connected_account_service(
        db=db,
        current_user=current_user,
        platform=platform,
        source_user_id=source_user_id
    )