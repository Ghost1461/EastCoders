from fastapi import APIRouter

router = APIRouter(
    prefix="/reports",
    tags=["Report"]
)

@router.get("/")
def dashboard_home():
    return {"message": "report çalışıyor"}