from typing import TYPE_CHECKING
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.user import User


class Token(Base):
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "user.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        unique=True,
        nullable=False,
        index=True,
    )
    access_token: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False,
        index=True,
    )
    refresh_token: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False,
        index=True,
    )

    # relationships
    user: Mapped["User"] = relationship(back_populates="token")
