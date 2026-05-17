import logging

from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.users.models import UserORM
from backend.src.users.schemas import UserCreate, UserResponse
from backend.src.users.service import UserService
from backend.src.database import async_pg_db_helper


logger = logging.getLogger(__name__)


router = APIRouter(tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
  user: UserCreate,
  session: AsyncSession = Depends(async_pg_db_helper.session_getter)
  ) -> UserORM:
  service = UserService(session)
  return await service.create_user(user)
