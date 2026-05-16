from fastapi import HTTPException
import bcrypt
from app.models.user_model import User

def serialize_user(user):
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "phone_number": user.phone_number,
        "profile_image_url": user.profile_image_url,
        "role": user.role,
        "created_at": user.created_at
    }


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def update_profile_service(request, db, current_user):
    update_data = request.model_dump(exclude_unset=True)#sadece gerçekten gönderilen alanları alır

    if "full_name" in update_data:
        current_user.full_name = update_data["full_name"]

    if "phone_number" in update_data:
        current_user.phone_number = update_data["phone_number"]

    if "profile_image_url" in update_data:
        current_user.profile_image_url = update_data["profile_image_url"]

    if "email" in update_data:
        new_email = update_data["email"]

        existing_user = db.query(User).filter(
            User.email == new_email,
            User.id != current_user.id
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="This email is already in use."
            )

        current_user.email = new_email

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Profile updated successfully.",
        "user": serialize_user(current_user)
    }


def change_password_service(request, db, current_user):
    current_password = request.current_password.strip()
    new_password = request.new_password.strip()
    new_password_confirm = request.new_password_confirm.strip()

    if not current_password or not new_password or not new_password_confirm:
        raise HTTPException(
            status_code=400,
            detail="Şifre alanları boş bırakılamaz."
        )

    if new_password != new_password_confirm:
        raise HTTPException(
            status_code=400,
            detail="Yeni şifreler eşleşmiyor."
        )

    if not verify_password(
        current_password,
        current_user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Geçerli parola yanlış."
        )

    if verify_password(
        new_password,
        current_user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Yeni şifre mevcut şifre ile aynı olamaz."
        )

    if len(new_password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Yeni şifre en az 6 karakter olmalıdır."
        )

    current_user.hashed_password = hash_password(new_password)

    db.commit()

    return {
        "message": "Şifre başarıyla değiştirildi."
    }