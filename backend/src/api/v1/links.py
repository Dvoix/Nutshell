from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from links.repository import LinkRepository
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.links.schemas import UrlIn, UrlOut
from backend.src.links.service import LinkService
from backend.src.database import async_pg_db_helper


router = APIRouter(tags=["Links"])


@router.post("/shorten", response_model=UrlOut, status_code=status.HTTP_201_CREATED)
async def create_slug(
    original: UrlIn,
    session: AsyncSession = Depends(async_pg_db_helper.session_getter)
    ) -> UrlOut:
    repo = LinkRepository(session)
    service = LinkService(repo)
    
    url = str(original.url)
    
    if len(url) > 2083:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="URL is too long")

    slug = await service.create_slug(url)
    return slug


@router.get("/{slug}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_by_slug(
    slug: str,
    session: AsyncSession = Depends(async_pg_db_helper.session_getter),
    ) -> RedirectResponse:
    repo = LinkRepository(session)
    service = LinkService(repo)
    
    redirect = await service.get_link_by_slug(slug)

    if redirect is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")

    return RedirectResponse(url=redirect.url)
