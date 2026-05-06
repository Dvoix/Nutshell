from sqlalchemy.orm import Mapped, mapped_column

from nutshell.models import Base, CreatedAtMixin, IntIdPkMixin

class links(IntIdPkMixin, CreatedAtMixin, Base):
  __tablename__ = "links"
  
  original_url: Mapped[str]
  short_code: Mapped[str] = mapped_column(unique=True)