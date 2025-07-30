from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Float, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.car.shared import Diametr
from .tire_enums import CarType, Season

if TYPE_CHECKING:
    from app.car.product import Product
    from ..tire_brand import TireBrand


class Tire(Base):

    tire_brand_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "tirebrand.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("product.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    diametr: Mapped[Diametr] = mapped_column(
        SqlEnum(Diametr),
        nullable=True,
    )
    width: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    height: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    index: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    car_type: Mapped[CarType] = mapped_column(
        SqlEnum(CarType),
        nullable=True,
    )
    model: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    season: Mapped[Season] = mapped_column(
        SqlEnum(Season),
        nullable=True,
    )
    residue: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )

    brand: Mapped["TireBrand"] = relationship(
        back_populates="tires",
    )
    product: Mapped["Product"] = relationship(
        back_populates="tire",
    )
