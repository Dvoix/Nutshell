import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.links.models import LinkORM

logger = logging.getLogger(__name__)


class LinkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, url: str, slug: str) -> LinkORM:
        link = LinkORM(
            url=str(url),
            slug=slug
        )

        self.session.add(link)
        await self.session.flush()
        return link

    async def get_by_slug(self, slug: str) -> LinkORM | None:
        result = await self.session.execute(
            select(LinkORM).where(LinkORM.slug == slug)
        )
        return result.scalar_one_or_none()

    async def delete(self, link: LinkORM) -> None:
        await self.session.delete(link)
