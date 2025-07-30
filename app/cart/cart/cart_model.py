from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.user import User
    from ..cart_items import CartItem


class Cart(Base):
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="CASCADE",
        ),
        index=True,
        unique=True,
        nullable=False,
    )

    # relationships
    user: Mapped["User"] = relationship(
        back_populates="cart",
    )

    items: Mapped[list["CartItem"]] = relationship(
        back_populates="cart",
        cascade="all, delete-orphan",
    )
