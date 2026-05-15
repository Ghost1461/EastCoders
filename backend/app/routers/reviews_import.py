from fastapi import APIRouter

router = APIRouter(
    prefix="/review_import",
    tags=["Review_Import"]
)

@router.get("/")
def dashboard_home():
    return {"message": "review çalışıyor"}