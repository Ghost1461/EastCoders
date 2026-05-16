from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User

from app.services.profile_services import (
    update_profile_service,
    change_password_service
)


router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


class ProfileUpdateRequest(BaseModel):
    full_name: str | None = None# string olabilir, null/boş olabilir, gönderilmeyebilir demek
    phone_number: str | None = None
    profile_image_url: str | None = None
    email: str | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str


@router.put("/update")
def update_profile(
    request: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_profile_service(
        request=request,
        db=db,
        current_user=current_user
    )


@router.put("/change-password")
def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return change_password_service(
        request=request,
        db=db,
        current_user=current_user
    )