from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def is_ok():
    return {"message": "Products route çalışıyor"}

@router.get("/return_pro")
def get_products():
    return [
        {"id": 1, "name": "Sweatshirt"},
        {"id": 2, "name": "Skirt"}
    ]