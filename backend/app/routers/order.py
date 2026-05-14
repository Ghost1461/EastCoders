from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.order_import_service import (
    import_orders_by_platform,
    import_all_orders,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/{platform_key}/import")
def import_platform_orders(platform_key: str, db: Session = Depends(get_db)):
    return import_orders_by_platform(db, platform_key)


@router.post("/import-all")
def import_orders(db: Session = Depends(get_db)):
    return import_all_orders(db)