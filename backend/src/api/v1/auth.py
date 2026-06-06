from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.src.auth.schemas import TokenInfo
from backend.src.auth.service import validate_auth_user
from backend.src.auth.utils import AuthService

from backend.src.dependencies.auth import get_auth_service
from backend.src.dependencies.users import get_user_service

from backend.src.users.models import User
from backend.src.users.schemas import UserCreate, UserResponse
from backend.src.users.service import UserService


router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    return await service.create_user(user)


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user: Annotated[User, Depends(validate_auth_user)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenInfo:
    jwt_payload = {
        "sub": user.id,
        "username": user.username,
    }
    token = service.encode_token(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
