from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import get_current_user
from app.models.user_model import User
from app.core.database import get_db
from app.schemas.auth import SignUpRequest, LoginRequest, AuthResponse
from app.services.authentication_service import AuthenticationService

router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"]
)

auth_service = AuthenticationService()


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

#Swagger Authorize için form login
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    class LoginRequest:
        email = form_data.username
        password = form_data.password

    try:
        return auth_service.login(LoginRequest, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    


#frontend/Postman/kendi login ekranın için JSON login
@router.post("/login-json", response_model=AuthResponse)
def login_json(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        return auth_service.login(request, db)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    

@router.post("/logout")
def logout():
    return auth_service.logout()

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)#token’dan user’ı çözüp service’e gönderiyor
):
    return auth_service.get_me(current_user)