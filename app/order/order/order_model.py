from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import func, String, ForeignKey, DateTime, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from .order_enums import OrderStatuses

if TYPE_CHECKING:
    from app.user import User
    from ..order_item import OrderItem


class Order(Base):

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="CASCADE",
        ),
        nullable=True,
        unique=False,
    )
    user_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=False,
    )
    user_phone: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=False,
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    city_to_ship: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    adress_to_ship: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    postal_code: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    status: Mapped[SqlEnum] = mapped_column(
        SqlEnum(OrderStatuses),
        nullable=False,
        default=OrderStatuses.PROCESSING,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="orders",
    )
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )
