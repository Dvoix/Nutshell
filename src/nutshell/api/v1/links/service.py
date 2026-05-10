import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from nutshell.api.v1.links.repository import LinkRepository
from nutshell.utils import generate_short_code
from nutshell.database.links.models import LinkORM

logger = logging.getLogger(__name__)


class LinkService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = LinkRepository(session)
        
    async def create_short_code(self, url: str, max_retries: int = 5) -> LinkORM:
        for attempt in range(max_retries):
            short_code = generate_short_code()
            
            try:
                link = await self.repo.create(url, short_code)
                await self.session.commit()
                return link
            
            
            except IntegrityError:
                await self.session.rollback()
                logger.warning(
                    f"Collision detected for code: {short_code}." 
                    f"Retrying... (Attempt {attempt + 1})")
                continue
            
        raise RuntimeError(
            f"Could not generate a unique short link after {max_retries} attempts."
        )
        
    async def redirect(self, short_code: str) -> LinkORM | None:
        redirect = await self.repo.get_by_code(short_code)
        
        if redirect is None:
            return None
        
        return redirect