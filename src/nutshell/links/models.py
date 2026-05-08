from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


from nutshell.mixins.models import Base, CreatedAtMixin, IdPrimaryKeyMixin


if TYPE_CHECKING:
    from nutshell.users.models import User


class Link(IdPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "links"

    original_url: Mapped[str] = mapped_column(nullable=False)

    short_code: Mapped[str] = mapped_column(
        String(16),
        unique=True,
        nullable=False
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    owner: Mapped["User"] = relationship(
        back_populates="links"
    )