from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.car_parts.car_brand import CarBrand
    from app.car_parts.car_brand_series_assoc import CarBrandPartSeriesAssoc


class CarSeries(Base):
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
    )
    year: Mapped[str] = mapped_column(
        String,
        unique=False,
    )

    brand_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("carbrand.id"),
        index=True,
        unique=False,
    )

    # relationship
    brand: Mapped["CarBrand"] = relationship(
        back_populates="series",
    )

    car_part: Mapped[list["CarBrandPartSeriesAssoc"]] = relationship(
        back_populates="series"
    )
