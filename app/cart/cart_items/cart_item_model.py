from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.car.product import Product
    from ..cart import Cart


class CartItem(Base):
    cart_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "cart.id",
            ondelete="CASCADE",
        ),
        index=True,
    )
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "product.id",
            ondelete="CASCADE",
        ),
        index=True,
    )

    cart: Mapped["Cart"] = relationship(
        back_populates="items",
    )
    product: Mapped["Product"] = relationship(
        back_populates="cart_items",
    )
