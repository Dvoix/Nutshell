from datetime import datetime

from sqlalchemy import func, MetaData, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from nutshell.utils import camel_case_to_snake_case
from nutshell.config import settings

class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"


class IdPrimaryKeyMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


def get_current_dt() -> datetime:
    dt = datetime.now()
    return dt


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        default=get_current_dt,
        server_default=func.now(),
        nullable=False,
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        default=get_current_dt,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class IsActiveMixin:
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default=text("true"),
        nullable=False
    )