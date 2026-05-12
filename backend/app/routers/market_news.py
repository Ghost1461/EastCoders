from fastapi import APIRouter

router = APIRouter(
    prefix="/news",
    tags=["News"]
)

@router.get("/")
def dashboard_home():
    return {"message": "news çalışıyor"}