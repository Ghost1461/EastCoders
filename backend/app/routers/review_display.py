from fastapi import APIRouter

router = APIRouter(
    prefix="/review_display",
    tags=["Review_Display"]
)

@router.get("/")
def dashboard_home():
    return {"message": "review çalışıyor"}