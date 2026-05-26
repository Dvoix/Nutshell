from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse


from backend.src.dependencies.links import get_link_service
from backend.src.links.schemas import UrlIn, UrlOut
from backend.src.links.service import LinkService


router = APIRouter(tags=["Links"])


@router.post("/shorten", response_model=UrlOut, status_code=status.HTTP_201_CREATED)
async def create_slug(
    original: UrlIn,
    service: LinkService = Depends(get_link_service),
    ) -> UrlOut:
    url = str(original.url)
    slug = await service.create_slug(url)
    
    if len(url) > 2083:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="URL is too long")
    
    return slug


@router.get("/{slug}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_by_slug(
    slug: str,
    service: LinkService = Depends(get_link_service)
    ) -> RedirectResponse:
    redirect = await service.get_link_by_slug(slug)

    if redirect is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")

    return RedirectResponse(url=redirect.url)
