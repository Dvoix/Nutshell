import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.enums import UserRole
from backend.src.users.models import User

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(
        self,
        username: str,
        email: str,
        password_hash: str,
    ) -> User:
        db_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
        )
        self.session.add(db_user)
        await self.session.flush()
        return db_user

    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id),
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email),
        )
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username),
        )
        return result.scalar_one_or_none()

    async def get_admin_user(self) -> User | None:
        result = await self.session.execute(
            select(User).where(User.role == UserRole.admin),
        )
        return result.scalar_one_or_none()
