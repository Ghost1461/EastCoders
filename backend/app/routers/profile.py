from fastapi import APIRouter
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User


router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get("/")
def dashboard_home():
    return {"message": "profile çalışıyor"}