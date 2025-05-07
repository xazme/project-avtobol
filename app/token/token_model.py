from typing import TYPE_CHECKING
from app.database import Base
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.user import User


class Token(Base):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), unique=True)
    access_token: Mapped[str] = mapped_column(
        Text,
        unique=True,
    )
    refresh_token: Mapped[str] = mapped_column(
        Text,
        unique=True,
    )

    # relationships
    user: Mapped["User"] = relationship(back_populates="token")
