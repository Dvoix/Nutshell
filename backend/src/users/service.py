import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.utils import AuthService
from backend.src.users.models import UserORM
from backend.src.users.repository import UserRepository
from backend.src.users.schemas import UserCreate


logger = logging.getLogger(__name__)


class UserService():
  def __init__(self, session: AsyncSession) -> None:
    self.session = session
    self.repo = UserRepository(session)
  
  async def create_user(self, user: UserCreate) -> UserORM:
    password_hash = AuthService.hash_password(user.password)
    try:
      user_obj = await self.repo.create(user, password_hash)
      
      await self.session.commit()
      
      return user_obj

    except IntegrityError:
      await self.session.rollback()
      logger.warning(
                f"Failed to create user: username={user.username}, email={user.email}"
            )
      raise
