from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.mixins.models import Base, CreatedAtMixin, IdPrimaryKeyMixin

if TYPE_CHECKING:
    from backend.src.users.models import User


class Link(IdPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "links"

    url: Mapped[str] = mapped_column(nullable=False)

    slug: Mapped[str] = mapped_column(
        String(16),
        unique=True,
        nullable=False
    )

    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    owner: Mapped["User"] = relationship(back_populates="links")
