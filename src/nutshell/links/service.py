import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from nutshell.links.repository import LinkRepository
from nutshell.links.models import LinkORM
from nutshell.utils import generate_slug

logger = logging.getLogger(__name__)


class LinkService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = LinkRepository(session)

    async def create_slug(self, url: str, max_retries: int = 5) -> LinkORM:
        for attempt in range(max_retries):
            slug = generate_slug()

            try:
                slug = await self.repo.create(url, slug)
                await self.session.commit()
                return slug

            except IntegrityError:
                await self.session.rollback()
                logger.warning(
                    f"Collision detected for code: {slug}."
                    f"Retrying... (Attempt {attempt + 1})")
                continue

        raise RuntimeError(
            f"Could not generate a unique slug after {max_retries} attempts."
        )

    async def get_link_by_slug(self, slug: str) -> LinkORM | None:
        return await self.repo.get_by_slug(slug)
