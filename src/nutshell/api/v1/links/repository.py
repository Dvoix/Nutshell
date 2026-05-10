import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nutshell.database.links.models import LinkORM


logger = logging.getLogger(__name__)


class LinkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def create(self, url: str, short_code: str) -> LinkORM:
        link = LinkORM(
            url=str(url),
            short_code=short_code
        )
        
        self.session.add(link)
        await self.session.flush()
        return link

    async def get_by_short_code(self, short_code: str) -> LinkORM | None:
        result = await self.session.execute(
            select(LinkORM).where(LinkORM.short_code == short_code)
        )
        return result.scalar_one_or_none()

    async def delete(self, link: LinkORM) -> None:
        await self.session.delete(link)
