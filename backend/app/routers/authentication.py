from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import SignUpRequest, LoginRequest, AuthResponse
from app.services.authentication_service import AuthenticationService

router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"]
)

auth_service = AuthenticationService()

@router.get("/")
def dashboard_home():
    return {"message": "authentication çalışıyor"}

@router.post("/signup", response_model=AuthResponse)
def signup(
    request: SignUpRequest,
    db: Session = Depends(get_db)
):
    try:
        return auth_service.signup(request, db)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/login", response_model=AuthResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        return auth_service.login(request, db)

    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )