from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from .order_item_enums import OrderItemStatus

if TYPE_CHECKING:
    from app.car.product import Product
    from ..order import Order


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

    status: Mapped[SqlEnum] = mapped_column(
        SqlEnum(OrderItemStatus),
        nullable=False,
        default=OrderItemStatus.PENDING,
    )

    # связи
    order: Mapped["Order"] = relationship(
        back_populates="order_items",
    )
    product: Mapped["Product"] = relationship(
        back_populates="order_items",
    )
