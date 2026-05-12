from fastapi import APIRouter

router = APIRouter(
    prefix="/alerts",
    tags=["Alert"]
)

@router.get("/")
def dashboard_home():
    return {"message": "alert çalışıyor"}