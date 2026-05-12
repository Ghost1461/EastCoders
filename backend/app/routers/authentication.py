from fastapi import APIRouter

router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"]
)

@router.get("/")
def dashboard_home():
    return {"message": "authentication çalışıyor"}