from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.user import User
    from app.car.product import Product


class Cart(Base):
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "user.id",
        ),
        nullable=False,
        index=True,
    )
    product_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "product.id",
        ),
        unique=False,
        nullable=False,
        index=True,
    )

    # relationship
    user: Mapped["User"] = relationship(
        back_populates="cart",
    )
    product: Mapped["Product"] = relationship(
        back_populates="cart",
    )
