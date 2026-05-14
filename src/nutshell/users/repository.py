import logging

from sqlalchemy.ext.asyncio import AsyncSession

from nutshell.users.models import UserORM
from nutshell.users.schemas import UserAuth


logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: UserAuth, password_hash: str) -> UserORM:
        user_obj = UserORM(
            username=user.username,
            email=user.email,
            password_hash=password_hash
        )

        self.session.add(user_obj)
        await self.session.flush()

        return user_obj
