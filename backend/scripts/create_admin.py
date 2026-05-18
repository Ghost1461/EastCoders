#Admin oluşturmak için ayrı bir terminal açıp 
#"docker compose exec backend python scripts/create_admin.py"
#komutunu çalıştırın, ve giriş yapın

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.core.database import SessionLocal
from app.models.user_model import User
from app.services.authentication_service import AuthenticationService

db = SessionLocal()

auth_service = AuthenticationService()


ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin"


existing_admin = db.query(User).filter(
    User.email == ADMIN_EMAIL
).first()


if existing_admin:
    print("Admin zaten mevcut.")
    exit()


hashed_password = auth_service.hash_password(
    ADMIN_PASSWORD
)


admin_user = User(
    full_name="System Admin",
    email=ADMIN_EMAIL,
    phone_number="0000000000",
    hashed_password=hashed_password,
    role="admin"
)


db.add(admin_user)
db.commit()


print("Admin başarıyla oluşturuldu.")