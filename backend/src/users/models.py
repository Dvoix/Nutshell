from typing import TYPE_CHECKING

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.enums import UserRole
from backend.src.mixins.models import (
    Base,
    CreatedAtMixin,
    IdPrimaryKeyMixin,
    IsActiveMixin,
    UpdatedAtMixin,
)

if TYPE_CHECKING:
    from backend.src.links.models import LinkORM


class UserORM(Base, IdPrimaryKeyMixin, CreatedAtMixin, UpdatedAtMixin, IsActiveMixin):
  __tablename__ = "users"

  username: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
  email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
  password_hash: Mapped[str] = mapped_column(String(255), unique=False, nullable=False)
  role: Mapped[UserRole] = mapped_column(
    Enum(UserRole),
    default=UserRole.user,
    nullable=False
    )

  links: Mapped[
    list["LinkORM"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
