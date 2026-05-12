from fastapi import APIRouter

router = APIRouter(
    prefix="/integrations",
    tags=["Integrations"]
)

@router.post("/integrations/trendyol/import-products")
def import_products():
    return {
        "message": "Products imported successfully"
    }