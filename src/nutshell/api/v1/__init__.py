from fastapi import APIRouter

from nutshell.config import settings

from nutshell.api.v1.links import router as links_router

router = APIRouter(
  prefix=settings.api.v1.prefix
)
router.include_router(
  links_router,
  prefix=settings.api.v1.links
)
