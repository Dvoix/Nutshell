from typing import TYPE_CHECKING

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nutshell.enums import UserRole
from nutshell.mixins.models import (
    Base,
    CreatedAtMixin,
    IdPrimaryKeyMixin,
    IsActiveMixin,
    UpdatedAtMixin,
)

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
    list["LinkORM"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
