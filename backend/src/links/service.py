import logging

from sqlalchemy.exc import IntegrityError

from backend.src.links.models import Link
from backend.src.links.repository import LinkRepository
from backend.src.utils import generate_slug

logger = logging.getLogger(__name__)


class LinkService:
    def __init__(self, repo: LinkRepository) -> None:
        self.repo = repo

    async def create_slug(self, url: str, max_retries: int = 5) -> Link:
        for attempt in range(max_retries):
            slug = generate_slug()

            try:
                return await self.repo.create_link(url, slug)

            except IntegrityError:
                logger.warning(
                    "Collision detected for code: %s. Retrying... (Attempt %s)",
                    slug,
                    attempt + 1,
                )
                continue

        raise RuntimeError(
            "Could not generate a unique short link after "
            f"{max_retries} attempts."
        )

    async def create_custom_slug(self, url: str, custom_slug: str) -> Link:
        try:
            custom_link = await self.repo.create_link_with_custom_slug(url, custom_slug)
        
        except IntegrityError as exc:
            logger.warning("Custom slug already exists: %s", custom_slug)
            
            raise ValueError("Custom slug already exists.") from exc

        return custom_link

    async def get_link_by_slug(self, slug: str) -> Link | None:
        return await self.repo.get_link_by_slug(slug)
