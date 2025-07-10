from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy import Float, ForeignKey, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from .engine_enums import GearboxType, FuelType

if TYPE_CHECKING:
    from app.car.product import Product


class Engine(Base):

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "product.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )
    engine_type: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    gearbox: Mapped[GearboxType] = mapped_column(
        SqlEnum(GearboxType),
        nullable=True,
    )
    fuel: Mapped[FuelType] = mapped_column(
        SqlEnum(FuelType),
        nullable=True,
    )
    volume: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    vin: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    product: Mapped["Product"] = relationship(
        back_populates="engine",
    )
