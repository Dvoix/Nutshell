import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from nutshell.links.repository import LinkRepository
from nutshell.utils import generate_short_code
from nutshell.links.models import LinkORM

logger = logging.getLogger(__name__)


class LinkService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = LinkRepository(session)

    async def create_short_link(self, original_url: str, max_retries: int = 5):
        for attempt in range(max_retries):
            short_code = generate_short_code()

            short_link = LinkORM(
                original_url=str(original_url),
                short_code=short_code
            )

            self.session.add(short_link)

            try:
                await self.session.commit()
                await self.session.refresh(short_link)
                return short_link

            except IntegrityError:
                await self.session.rollback()
                logger.warning(
                    f"Collision detected for code: {short_code}. Retrying... (Attempt {attempt + 1})")
                continue

        raise RuntimeError(
            f"Could not generate a unique short link after {max_retries} attempts."
        )