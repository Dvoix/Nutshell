from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from nutshell.database import db_helper

from nutshell.api.v1.links.repository import LinkORM
from nutshell.api.v1.links.service import LinkService
from nutshell.api.v1.links.schemas import UrlIn, UrlOut


router = APIRouter(tags=["Links"])


@router.post("/shorten", response_model=UrlOut, status_code=status.HTTP_201_CREATED)
async def create_short_link(
  original: UrlIn, 
  session: AsyncSession = Depends(db_helper.session_getter)
) -> LinkORM:
  service = LinkService(session)
  short_code = await service.create_short_code(str(original.url))
  
  
  if len(str(original)) > 2083:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="URL is too long")
        
        
  existing = None
  
  if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Short URL already exists")
        
        
  if short_code is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not generate unique short code")
            
  return short_code


