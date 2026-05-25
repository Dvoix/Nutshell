import logging

from sqlalchemy.exc import IntegrityError

from backend.src.users.repository import UserRepository
from backend.src.auth.utils import AuthService
from backend.src.users.models import User
from backend.src.users.schemas import UserCreate


logger = logging.getLogger(__name__)


class UserService():
  def __init__(self, repo: UserRepository) -> None:
    self.repo = repo
  
  async def create_user(self, user: UserCreate) -> User:
    password_hash = AuthService.hash_password(user.password)
    try:
      user = await self.repo.create_user(user, password_hash)
      return user

    except IntegrityError:
      logger.warning(
                f"Failed to create user: username={user.username}, email={user.email}"
            )
      raise

  async def get_user_by_id(self, user_id: int) -> User | None:
    return await self.repo.get_user_by_id(user_id)

  async def get_user_by_email(self, email: str) -> User | None:
    return await self.repo.get_user_by_email(email)
