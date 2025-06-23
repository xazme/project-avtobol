import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models"""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
