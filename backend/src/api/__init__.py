from fastapi import APIRouter

from backend.src.config import settings

from .v1 import router as api_v1_router

router = APIRouter(prefix=settings.api.prefix)
router.include_router(api_v1_router)
