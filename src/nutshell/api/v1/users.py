import logging

from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from nutshell.users.models import UserORM
from nutshell.users.schemas import UserCreate, UserResponse
from nutshell.users.service import UserService
from nutshell.database import db_helper


logger = logging.getLogger(__name__)


router = APIRouter(tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
  user: UserCreate,
  session: AsyncSession = Depends(db_helper.session_getter)
  ) -> UserORM:
  service = UserService(session)
  return await service.create_user(user)
