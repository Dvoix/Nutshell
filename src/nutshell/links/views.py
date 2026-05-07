from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from nutshell.database import db_helper

from nutshell.links.models import Link
from nutshell.links.repository import create_short_link
from nutshell.links.schemas import URLCreate, URLOut


router = APIRouter()

@router.post("/shorten", response_model=URLOut, status_code=status.HTTP_201_CREATED)
async def short_link_response(
  data: URLCreate, 
  session: AsyncSession = Depends(db_helper.session_getter)
)-> dict[str, Link]:
  
  short_code = await create_short_link(session, data)
  if not short_code:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
      detail="Could not generate unique short code try again")
  
  return {"short_code": short_code}