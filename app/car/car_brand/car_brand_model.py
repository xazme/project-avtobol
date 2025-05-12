from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.car.car_series import CarSeries

    # from app.car.car_brand_series_assoc import CarBrandPartSeriesAssoc


class CarBrand(Base):
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
    )
    picture: Mapped[str] = mapped_column(
        String,
        unique=True,
    )

    # relationship
    # series: Mapped[List["CarSeries"]] = relationship(
    #     back_populates="brand",
    # )

    # car_part: Mapped["CarBrandPartSeriesAssoc"] = relationship(
    #     back_populates="brand",
    # )
