from pydantic import (
    BaseModel,
    EmailStr,
    field_validator
)


class SignUpRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    password: str
    password_confirm: str

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Ad soyad en az 2 karakter olmalıdır."
            )

        if len(value) > 61:
            raise ValueError(
                "Ad soyad en fazla 61 karakter olabilir."
            )

        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):

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

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if len(value) < 6:
            raise ValueError(
                "Şifre en az 6 karakter olmalıdır."
            )

        if len(value) > 35:
            raise ValueError(
                "Şifre en fazla 35 karakter olabilir."
            )

        if not any(char.isupper() for char in value):
            raise ValueError(
                "Şifre en az bir büyük harf içermelidir."
            )

        if not any(char.islower() for char in value):
            raise ValueError(
                "Şifre en az bir küçük harf içermelidir."
            )

        if not any(char.isdigit() for char in value):
            raise ValueError(
                "Şifre en az bir rakam içermelidir."
            )

        return value
    
    @field_validator("password_confirm")
    @classmethod
    def validate_password_confirm(cls, value):

        if len(value) < 6:
            raise ValueError("Şifre tekrarı en az 6 karakter olmalıdır.")

        if len(value) > 35:
            raise ValueError("Şifre tekrarı en fazla 35 karakter olabilir.")

        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if len(value.strip()) == 0:
            raise ValueError(
                "Şifre boş bırakılamaz."
            )

        return value
    


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone_number: str
    role: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse