from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.product_import_service import (
    import_products_by_platform,
    import_all_products
)


router = APIRouter(
    prefix="/integrations",
    tags=["Integrations"]
)


@router.post("/{platform_key}/import-products")
def import_platform_products(
    platform_key: str,
    db: Session = Depends(get_db)
):
    return import_products_by_platform(db, platform_key)


@router.post("/import-products/all")
def import_all_platform_products(db: Session = Depends(get_db)):
    return import_all_products(db)