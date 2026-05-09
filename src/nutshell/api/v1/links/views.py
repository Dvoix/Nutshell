from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from nutshell.database import db_helper

from nutshell.api.v1.links.repository import LinkORM
from nutshell.api.v1.links.service import LinkService
from nutshell.api.v1.links.schemas import UrlIn, UrlOut


router = APIRouter()

@router.post("/shorten", response_model=UrlOut, status_code=status.HTTP_201_CREATED)
async def create_short_link(
  original: UrlIn, 
  session: AsyncSession = Depends(db_helper.session_getter)
) -> LinkORM:
  service = LinkService(session)
  short_code = await service.create_short_code(str(original.url))
  
  if not short_code:
    
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
      detail="Could not generate unique short code try again")
  
  return short_code