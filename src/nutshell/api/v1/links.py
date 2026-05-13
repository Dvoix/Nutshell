import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession

from nutshell.links.schemas import UrlIn, UrlOut
from nutshell.links.service import LinkService
from nutshell.database import db_helper

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Links"])


@router.post("/shorten", response_model=UrlOut, status_code=status.HTTP_201_CREATED)
async def create_slug(
    original: UrlIn,
    session: AsyncSession = Depends(db_helper.session_getter)
    ) -> UrlOut:
    url = str(original.url)
    
    if len(url) > 2083:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="URL is too long")

    service = LinkService(session)
    slug = await service.create_slug(url)

    return slug


@router.get("/{slug}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_by_slug(
    slug: str,
    session: AsyncSession = Depends(db_helper.session_getter),
    ) -> RedirectResponse:
    service = LinkService(session)
    redirect = await service.get_link_by_slug(slug)

    if redirect is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")

    return RedirectResponse(url=redirect.url)
