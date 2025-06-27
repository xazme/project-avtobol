from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, func, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from .order_enums import OrderStatuses

if TYPE_CHECKING:
    from app.user import User
    from app.car.product import Product


class Order(Base):
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "user.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=True,
        index=True,
    )
    product_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "product.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        index=True,
    )
    user_name: Mapped[str] = mapped_column(
        String,
        nullable=True,
        unique=False,
    )
    user_phone: Mapped[str] = mapped_column(
        String,
        nullable=True,
        unique=False,
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    status: Mapped[SqlEnum] = mapped_column(
        SqlEnum(OrderStatuses),
        nullable=False,
        default=OrderStatuses.OPEN,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    # relationships
    product: Mapped["Product"] = relationship(
        back_populates="order",
    )
    user: Mapped["User"] = relationship(
        back_populates="order",
    )
