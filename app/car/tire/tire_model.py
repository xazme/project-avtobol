from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.car.product import Product


class TireBrand(Base):
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=False,
        index=True,
    )
    product: Mapped["Product"] = relationship(
        back_populates="tire_brand",
        cascade="all,delete-orphan",
    )
