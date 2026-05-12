from fastapi import APIRouter

router = APIRouter(
    prefix="/trends",
    tags=["Trend"]
)

@router.get("/")
def dashboard_home():
    return {"message": "trend çalışıyor"}