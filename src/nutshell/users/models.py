from typing import List, TYPE_CHECKING


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum

from nutshell.mixins.models import (
  Base, 
  IdPrimaryKeyMixin, 
  CreatedAtMixin, 
  UpdatedAtMixin, 
  IsActiveMixin
  )

from nutshell.enums import UserRole


if TYPE_CHECKING:
    from nutshell.links.models import LinkORM


class UserORM(Base, IdPrimaryKeyMixin, CreatedAtMixin, UpdatedAtMixin, IsActiveMixin):
  __tablename__ = "users"
  
  username: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
  email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
  role: Mapped[UserRole] = mapped_column(
    Enum(UserRole), 
    default=UserRole.user, 
    nullable=False
    )
  
  links: Mapped[
    List["LinkORM"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
