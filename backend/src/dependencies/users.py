from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.users.service import UserService
from backend.src.users.repository import UserRepository
from backend.src.database import async_pg_db_helper


async def get_user_repository(
    session: AsyncSession = Depends(async_pg_db_helper.session_getter),
) -> UserRepository:
    return UserRepository(session)


async def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)
