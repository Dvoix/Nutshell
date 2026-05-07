from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


from nutshell.mixins.models import Base, CreatedAtMixin, IdPrimaryKeyMixin
class Link(IdPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "links"

    original_url: Mapped[str] = mapped_column(nullable=False)
    short_code: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)