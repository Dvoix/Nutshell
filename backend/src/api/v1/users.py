from fastapi import APIRouter, HTTPException, status, Depends


from backend.src.dependencies.users import get_user_service
from backend.src.users.schemas import UserCreate, UserResponse
from backend.src.users.service import UserService


router = APIRouter(tags=["Users"])


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

@router.get("/id/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(
  user_id: int,
  service: UserService = Depends(get_user_service)
  ) -> UserResponse:
  user = await service.get_user_by_id(user_id)
  
  if user is None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User with that id doesn't exist"
    )
  
  return {
    "id": user.id,
    "username": user.username,
    "email": user.email,
    "role": user.role,
}


@router.get("/by-email", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_email(
    email: str,
    service: UserService = Depends(get_user_service),
  ) -> UserResponse:
  user = await service.get_user_by_email(email)

  if user is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User not found"
        )

  return {
    "id": user.id,
    "username": user.username,
    "email": user.email,
    "role": user.role,
}
