from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from backend.src.dependencies.links import get_link_service
from backend.src.links.schemas import CustomUrlIn, CustomUrlOut, UrlIn, UrlOut
from backend.src.links.service import LinkService

router = APIRouter(tags=["Links"])


@router.post("/shorten", response_model=UrlOut, status_code=status.HTTP_201_CREATED)
async def create_slug(
    original: UrlIn,
    service: Annotated[LinkService, Depends(get_link_service)],
) -> UrlOut:
    url = str(original.url)

    if len(url) > 2083:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="URL is too long",
        )

    return await service.create_slug(url)


@router.post("/custom-url", response_model=CustomUrlOut, status_code=status.HTTP_201_CREATED)
async def create_custom_url(
    custom_url: CustomUrlIn,
    service: Annotated[LinkService, Depends(get_link_service)],
) -> CustomUrlOut:
    url = str(custom_url.url)
    custom_slug = str(custom_url.custom_slug)

    if len(url) > 2083:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="URL is too long",
        )

    try:
        result = await service.create_custom_slug(url, custom_slug)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return result


@router.get("/{slug}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_by_slug(
    slug: str,
    service: Annotated[LinkService, Depends(get_link_service)],
) -> RedirectResponse:
    redirect = await service.get_link_by_slug(slug)

    if redirect is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found",
        )

    return RedirectResponse(url=redirect.url)
