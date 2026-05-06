import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from nutshell.Utils import generate_short_link
from .models import links

logger = logging.getLogger(__name__)

async def create_short_link(session: AsyncSession, original_url: str, max_retries: int = 5):
    for attempt in range(max_retries):
        short_code = generate_short_link()
        
        new_link = links(
            original_url=str(original_url),
            short_code=short_code
        )
        
        session.add(new_link)
        
        try:
            await session.commit()
            await session.refresh(new_link)
            return new_link
        
        except IntegrityError:
            await session.rollback()
            logger.warning(
              f"Collision detected for code: {short_code}. Retrying... (Attempt {attempt + 1})")
            continue

    raise RuntimeError(f"Could not generate a unique short link after {max_retries} attempts.")