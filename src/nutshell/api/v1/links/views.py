import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession

from nutshell.api.v1.links.schemas import UrlIn, UrlOut
from nutshell.api.v1.links.service import LinkService
from nutshell.database import db_helper

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Links"])


@router.post("/shorten", response_model=UrlOut, status_code=status.HTTP_201_CREATED)
async def create_short_link(
    original: UrlIn,
    session: AsyncSession = Depends(db_helper.session_getter)
    ) -> UrlOut:
    url = str(original.url)
    
    if len(url) > 2083:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="URL is too long")

    service = LinkService(session)
    short_code = await service.create_short_code(url)

    return short_code


@router.get("/{short_code}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_by_short_code(
    short_code: str,
    session: AsyncSession = Depends(db_helper.session_getter),
    ) -> RedirectResponse:
    service = LinkService(session)
    redirect = await service.get_link_by_short_code(short_code)

    if redirect is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")

    return RedirectResponse(url=redirect.url)
