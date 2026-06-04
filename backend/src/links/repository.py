import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.links.models import Link

logger = logging.getLogger(__name__)


class LinkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_link(self, url: str, slug: str) -> Link:
        link = Link(
            url=str(url), 
            slug=slug
        )
        self.session.add(link)
        await self.session.flush()
        return link

    async def create_link_with_custom_slug(self, url: str, custom_slug: str) -> Link:
        custom_link = Link(
            url=str(url),
            slug=custom_slug,
            custom_slug=custom_slug,
        )
        self.session.add(custom_link)
        await self.session.flush()
        return custom_link

    async def get_link_by_slug(self, slug: str) -> Link | None:
        result = await self.session.execute(
            select(Link).where(Link.slug == slug)
        )
        return result.scalar_one_or_none()

    async def delete_link(self, link: Link) -> None:
        self.session.delete(link)
