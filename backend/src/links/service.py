import logging

from sqlalchemy.exc import IntegrityError

from backend.src.links.repository import LinkRepository
from backend.src.links.models import Link
from backend.src.utils import generate_slug


logger = logging.getLogger(__name__)


class LinkService:
    def __init__(self, repo: LinkRepository) -> None:
        self.repo = repo

    async def create_slug(self, url: str, max_retries: int = 5) -> Link:
        for attempt in range(max_retries):
            slug = generate_slug()

            try:
                link = await self.repo.create_link(url, slug)
                return link

            except IntegrityError:
                logger.warning(
                    f"Collision detected for code: {slug}."
                    f"Retrying... (Attempt {attempt + 1})")
                continue

        raise RuntimeError(
            f"Could not generate a unique short link after {max_retries} attempts."
        )

    async def get_link_by_slug(self, slug: str) -> Link | None:
        return await self.repo.get_link_by_slug(slug)
