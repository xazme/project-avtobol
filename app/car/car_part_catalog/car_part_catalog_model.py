from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.car.product import Product


class CarPart(Base):
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    product: Mapped[List["Product"]] = relationship(
        back_populates="car_part",
        cascade="all,delete-orphan",
    )
