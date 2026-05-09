from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


from nutshell.mixins.models import Base, CreatedAtMixin, IdPrimaryKeyMixin


if TYPE_CHECKING:
    from nutshell.database.users.models import UserORM


class LinkORM(IdPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "links"

    url: Mapped[str] = mapped_column(nullable=False)

    short_code: Mapped[str] = mapped_column(
        String(16),
        unique=True,
        nullable=False
    )

    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    owner: Mapped["UserORM"] = relationship(back_populates="links")