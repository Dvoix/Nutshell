from typing import TYPE_CHECKING

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.enums import UserRole, UserStatus
from backend.src.mixins.models import (
    Base,
    CreatedAtMixin,
    IdPrimaryKeyMixin,
    UpdatedAtMixin,
)

if TYPE_CHECKING:
    from backend.src.links.models import Link


class User(Base, IdPrimaryKeyMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        index=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name='userrole'),
        default=UserRole.user,
        nullable=False,
    )

    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name='userstatus'),
        default=UserStatus.active,
        nullable=False,
    )

    links: Mapped[list['Link']] = relationship(
        back_populates='owner',
        cascade='all, delete-orphan',
    )
