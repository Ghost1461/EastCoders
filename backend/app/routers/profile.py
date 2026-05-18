from fastapi import APIRouter, Depends
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator
)
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
    full_name: str | None = None
    phone_number: str | None = None
    profile_image_url: str | None = None
    email: EmailStr | None = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):

        if value is None:
            return value

        if len(value.strip()) < 2:
            raise ValueError(
                "Ad soyad en az 2 karakter olmalıdır."
            )

        if len(value.strip()) > 61:
            raise ValueError(
                "Ad soyad en fazla 61 karakter olabilir."
            )

        return value.strip()

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):

        if value is None:
            return value

        value = value.strip()

        if len(value) < 10:
            raise ValueError(
                "Telefon numarası en az 10 karakter olmalıdır."
            )

        if len(value) > 20:
            raise ValueError(
                "Telefon numarası en fazla 20 karakter olabilir."
            )

        return value


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value):

        if len(value) < 6:
            raise ValueError(
                "Yeni şifre en az 6 karakter olmalıdır."
            )

        if len(value) > 35:
            raise ValueError(
                "Yeni şifre en fazla 35 karakter olabilir."
            )

        if not any(char.isupper() for char in value):
            raise ValueError(
                "Yeni şifre en az bir büyük harf içermelidir."
            )

        if not any(char.islower() for char in value):
            raise ValueError(
                "Yeni şifre en az bir küçük harf içermelidir."
            )

        if not any(char.isdigit() for char in value):
            raise ValueError(
                "Yeni şifre en az bir rakam içermelidir."
            )

        return value



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