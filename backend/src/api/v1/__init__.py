from fastapi import APIRouter

from backend.src.config import settings

from backend.src.api.v1.links import router as links_router
from backend.src.api.v1.users import router as users_router

router = APIRouter(
  prefix=settings.api.v1.prefix
)
router.include_router(
  links_router,
  prefix=settings.api.v1.links
)


router.include_router(
  users_router, 
  prefix=settings.api.v1.users
)