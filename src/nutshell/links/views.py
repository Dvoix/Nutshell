
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from nutshell.database import db_helper


from .repository import create_short_link
from .schemas import URLCreate, URLOut

router = APIRouter()

@router.post("/shorten", response_model=URLOut)
async def create_short_link_response(
  data: URLCreate, 
  session: Annotated[
		AsyncSession,
  Depends(db_helper.session_getter),
  ],
):
  short_code = await create_short_link(session, data)
  return {"short_code": short_code}