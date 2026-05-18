from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.admin_security import get_current_admin
from app.models.user_model import User

from app.services.admin_services import (
    get_all_users_service,
    get_user_detail_service,
    get_ai_cache_records_service,
    delete_ai_cache_record_service,
    get_admin_summary_service,
    delete_user_ai_cache_service,
    get_all_connected_accounts_service,
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# Sistemde kayıtlı tüm kullanıcıları listeler
@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    return get_all_users_service(db)


# Belirli bir kullanıcının detaylarını getirir
# Connected accountları ve AI cache sayısını da döner
@router.get("/users/{user_id}")
def get_user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    return get_user_detail_service(user_id, db)


# Sistemdeki tüm AI cache kayıtlarını listeler
@router.get("/ai-cache")
def get_ai_cache_records(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    return get_ai_cache_records_service(db)


# Belirli bir AI cache kaydını siler
@router.delete("/ai-cache/{cache_id}")
def delete_ai_cache_record(
    cache_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    return delete_ai_cache_record_service(cache_id, db)


# Admin dashboard özet verilerini döner
# Toplam user, connected account ve AI cache sayısı gibi
@router.get("/summary")
def get_admin_summary(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    return get_admin_summary_service(db)


# Belirli bir kullanıcıya ait tüm AI cache kayıtlarını siler
@router.delete("/users/{user_id}/ai-cache")
def delete_user_ai_cache(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    return delete_user_ai_cache_service(user_id, db)


# Sistemdeki tüm connected accountları listeler
# İstenirse platform filtrelemesi yapılabilir
@router.get("/connected-accounts")
def get_all_connected_accounts(
    platform: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    return get_all_connected_accounts_service(db, platform)