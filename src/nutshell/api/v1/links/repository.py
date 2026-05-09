from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nutshell.database.links.models import LinkORM


class LinkRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, original_url: str) -> LinkORM:
        link = LinkORM(original_url=str(original_url))

        self.session.add(link)

        await self.session.flush()

        return link
    
    async def get_by_code(self, short_code: str) -> LinkORM | None:
        result = await self.session.execute(
            select(LinkORM).where(LinkORM.short_code == short_code)
        )
        return result.scalar_one_or_none()

    async def delete(self, link: LinkORM) -> None:
        await self.session.delete(link)
