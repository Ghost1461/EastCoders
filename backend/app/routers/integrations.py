from fastapi import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.mock_import_service import import_hepsiburada_products

router = APIRouter(
    prefix="/integrations",
    tags=["Integrations"]
)

@router.post("/hepsiburada/import-products")
def import_hepsiburada(db: Session = Depends(get_db)):
    return import_hepsiburada_products(db)