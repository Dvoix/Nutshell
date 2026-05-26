from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.links.service import LinkService
from backend.src.links.repository import LinkRepository
from backend.src.database import async_pg_db_helper


async def get_link_repository(
    session: AsyncSession = Depends(async_pg_db_helper.session_getter),
) -> LinkRepository:
    return LinkRepository(session)


async def get_link_service(
    repo: LinkRepository = Depends(get_link_repository),
) -> LinkService:
    return LinkService(repo)
