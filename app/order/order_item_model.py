from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.car.product import Product
    from .order_model import Order


class OrderItem(Base):

    order_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "order.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=False,
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "product.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=False,
    )

    # связи
    order: Mapped["Order"] = relationship(
        back_populates="order_items",
    )
    product: Mapped["Product"] = relationship(
        back_populates="order_items",
    )
