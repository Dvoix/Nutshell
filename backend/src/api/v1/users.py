from fastapi import APIRouter, status, Depends


from backend.src.dependencies.users import get_user_service
from backend.src.users.models import User
from backend.src.users.schemas import UserCreate, UserResponse
from backend.src.users.service import UserService


router = APIRouter(tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
  user: UserCreate,
  service: UserService = Depends(get_user_service)
  ) -> User:
  return await service.create_user(user)
