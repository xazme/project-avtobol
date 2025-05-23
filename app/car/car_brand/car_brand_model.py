from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.car.car_series import CarSeries
    from app.car.product import Product


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
    car_series: Mapped[List["CarSeries"]] = relationship(
        back_populates="car_brand",
    )

    car_part: Mapped["Product"] = relationship(
        back_populates="car_brand",
    )
