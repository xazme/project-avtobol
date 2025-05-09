from sqlalchemy import Integer, BigInteger
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)
import uuid
from app.core.config import settings


def generate_id():
    id = uuid.uuid4()
    new_id = int(id) >> 100
    return new_id


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models"""

    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        primary_key=True,
        index=True,
        default=generate_id,
    )
