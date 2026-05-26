from fastapi import APIRouter, HTTPException, status, Depends

from backend.src.auth.service import validate_auth_user
from backend.src.dependencies.auth import get_auth_service
from backend.src.dependencies.users import get_user_service
from backend.src.users.schemas import UserCreate, UserResponse
from backend.src.users.service import UserService

from backend.src.auth.utils import AuthService
from backend.src.auth.schemas import LoginRequest, TokenInfo


router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate,
    service: UserService = Depends(get_user_service)
    ) -> UserResponse:
    user = await service.create_user(user)
    
    return {
    "id": user.id,
    "username": user.username,
    "email": user.email,
    "role": user.role,
}


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user: LoginRequest = Depends(validate_auth_user),
    service: AuthService = Depends(get_auth_service)
):
    jwt_payload = {
        "sub": user.id,
        "username": user.username,
    }
    token = service.encode_token(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )