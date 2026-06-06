from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.src.dependencies.users import get_user_service
from backend.src.users.models import User
from backend.src.users.schemas import UserResponse
from backend.src.users.service import UserService


router = APIRouter(tags=["Users"])


@router.get("/id/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    user = await service.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with that id doesn't exist",
        )

    return user


@router.get("/by-email", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_email(
    email: str,
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    user = await service.get_user_by_email(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
