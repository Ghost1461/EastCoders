from datetime import datetime, timedelta
import bcrypt
from jose import jwt
from sqlalchemy.orm import Session

from app.models.user_model import User


SECRET_KEY = "change-this-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class AuthenticationService:

    def hash_password(self, password: str) -> str:
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        return hashed_password.decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        plain_password_bytes = plain_password.encode("utf-8")
        hashed_password_bytes = hashed_password.encode("utf-8")

        return bcrypt.checkpw(
            plain_password_bytes,
            hashed_password_bytes
        )

    def create_access_token(self, data: dict) -> str:
        payload = data.copy()

        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload.update({"exp": expire})

        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    def signup(self, request, db: Session):
        if request.password != request.password_confirm:
            raise ValueError("Şifreler eşleşmiyor.")

        existing_user = db.query(User).filter(
            User.email == request.email
        ).first()

        if existing_user:
            raise ValueError("Bu e-posta zaten kayıtlı.")

        hashed_password = self.hash_password(request.password)

        new_user = User(
            full_name=request.full_name,
            email=request.email,
            phone_number=request.phone_number,
            hashed_password=hashed_password,
            role="seller"
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        access_token = self.create_access_token({
            "sub": str(new_user.id),
            "role": new_user.role
        })

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": new_user.id,
                "full_name": new_user.full_name,
                "email": new_user.email,
                "phone_number": new_user.phone_number,
                "role": new_user.role
            }
        }

    def login(self, request, db: Session):
        email = getattr(request, "email", None) or getattr(request, "username", None)

        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user:
            raise ValueError("E-posta veya şifre hatalı.")

        password_is_valid = self.verify_password(
            request.password,
            user.hashed_password
        )

        if not password_is_valid:
            raise ValueError("E-posta veya şifre hatalı.")

        access_token = self.create_access_token({
            "sub": str(user.id),
            "role": user.role
        })

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "role": user.role
            }
    }

    def logout(self):
        return {
            "message": "Başarıyla çıkış yapıldı."
        }
    
    def get_me(self, current_user: User):
        return {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "phone_number": current_user.phone_number,
            "role": current_user.role,
            "profile_image_url": current_user.profile_image_url
        }