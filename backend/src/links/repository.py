import logging
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.links.models import LinkORM

logger = logging.getLogger(__name__)


class LinkRepositoryProtocol(Protocol):
    async def create_link_obj(self, url: str, slug: str) -> object:
        ...
    
    async def get_link_by_slug(self, slug: str) -> object | None:
        ...
    
    async def delete_link_obj(self, link_obj: object) -> None:
        ...


class LinkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_link_obj(self, url: str, slug: str) -> LinkORM:
        link_obj = LinkORM(
            url=str(url),
            slug=slug
        )
        self.session.add(link_obj)
        await self.session.flush()
        return link_obj

    async def get_link_obj_by_slug(self, slug: str) -> LinkORM | None:
        result = await self.session.execute(
            select(LinkORM).where(LinkORM.slug == slug)
        )
        return result.scalar_one_or_none()

    async def delete_link_obj(self, link_obj: LinkORM) -> None:
        self.session.delete(link_obj)
