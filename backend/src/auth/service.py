from typing import Annotated

from backend.src.enums import UserStatus
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.src.auth.utils import AuthService
from backend.src.dependencies.auth import get_auth_service
from backend.src.dependencies.users import get_user_service
from backend.src.users.models import User
from backend.src.users.service import UserService


async def validate_auth_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service)
    ) -> User:
    user = await user_service.get_user_by_username(form_data.username)

    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    
    if not user:
        raise unauthed_exc

    if not auth_service.check_password(form_data.password, user.password_hash):
        raise unauthed_exc
    
    if user.status != UserStatus.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user
