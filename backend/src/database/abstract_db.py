from abc import ABC, abstractmethod

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

class AbstractDataBaseProvider(ABC):
  @abstractmethod
  async def dispose(self) -> None:
    ...
  
  @abstractmethod
  async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
    ...
