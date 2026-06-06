from typing import Annotated

from fastapi import Depends

from backend.src.auth.utils import AuthService


async def get_auth_service(
    service: Annotated[AuthService, Depends(AuthService)],
) -> AuthService:
    return service
