import logging

from sqlalchemy.ext.asyncio import AsyncSession

from nutshell.users.models import UserORM
from nutshell.users.schemas import UserCreate


logger = logging.getLogger(__name__)


class UserRepository:
  def __init__(self, session: AsyncSession) -> None:
    self.session = session
    
    async def create(self, user: UserCreate) -> User:
      hashed_password = get_password_hash(user.password) 
      user = 