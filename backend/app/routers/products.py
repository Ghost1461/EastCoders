from fastapi import APIRouter

router = APIRouter()

@router.get("/products")
def get_products():
    return [
        {"id": 1, "name": "Sweatshirt"},
        {"id": 2, "name": "Skirt"}
    ]