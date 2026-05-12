from fastapi import APIRouter

router = APIRouter()

@router.get("/products")
def get_products():
    return [
        {"id": 1, "name": "iPhone 15"},
        {"id": 2, "name": "Samsung S24"}
    ]