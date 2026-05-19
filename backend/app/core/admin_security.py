#aktif user'ın role'u admin mi diye kontrol
from fastapi import Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.user_model import User


def get_current_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu işlem için admin yetkisi gerekli."
        )

    return current_user