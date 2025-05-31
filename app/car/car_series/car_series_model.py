from typing import TYPE_CHECKING, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.car.car_brand import CarBrand
    from app.car.product import Product


class CarSeries(Base):
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
    )
    year: Mapped[str] = mapped_column(
        String,
        unique=False,
    )

    car_brand_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "carbrand.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        index=True,
        unique=False,
    )

    # relationship
    car_brand: Mapped["CarBrand"] = relationship(
        back_populates="car_series",
        single_parent=True,
    )

    product: Mapped[List["Product"]] = relationship(
        back_populates="car_series",
        cascade="all,delete-orphan",
    )
