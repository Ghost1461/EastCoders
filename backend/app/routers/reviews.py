from fastapi import APIRouter

router = APIRouter(
    prefix="/reviews",
    tags=["Review"]
)

@router.get("/")
def dashboard_home():
    return {"message": "review çalışıyor"}