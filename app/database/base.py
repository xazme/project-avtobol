from sqlalchemy import Integer
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)
from app.core.config import settings


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models"""

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
