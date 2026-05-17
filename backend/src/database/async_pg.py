import logging
from collections.abc import AsyncGenerator

from database.abstract_db import AbstractDataBaseProvider
from sqlalchemy.ext.asyncio import (
  AsyncEngine,
  AsyncSession,
  async_sessionmaker,
  create_async_engine,
)

from backend.src.config import settings

log = logging.getLogger(__name__)


class AsyncPgDatabaseHelper(AbstractDataBaseProvider):
  def __init__(
    self,
    url: str,
    echo: bool = False,
    echo_pool: bool = False,
    max_overflow: int = 10,
    pool_size: int = 5
  ) -> None:
    self.engine: AsyncEngine = create_async_engine(
      url=url,
      echo=echo,
      echo_pool=echo_pool,
      max_overflow=max_overflow,
      pool_size=pool_size,
    )
    self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
      bind=self.engine,
      autoflush=False,
      expire_on_commit=False,
      )

  async def dispose(self) -> None:
    await self.engine.dispose()

  async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
    async with self.session_factory() as session:
      try:
        yield session
        await session.commit()
      
      except:
        await session.rollback()
        raise


async_pg_db_helper = AsyncPgDatabaseHelper(
url=str(settings.db.url),
echo=settings.db.echo,
echo_pool=settings.db.echo_pool,
max_overflow=settings.db.max_overflow,
pool_size=settings.db.pool_size
)
