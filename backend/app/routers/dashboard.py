from fastapi import APIRouter

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/")
def dashboard_home():
    return {"message": "dashboard çalışıyor"}