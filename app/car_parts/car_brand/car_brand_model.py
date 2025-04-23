from typing import TYPE_CHECKING, List
from sqlalchemy import String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.car_parts.car_series import CarSeries


class CarBrand(Base):
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
    )
    url: Mapped[str] = mapped_column(
        String,
        unique=True,
    )

    # relationship
    series: Mapped[List["CarSeries"]] = relationship(
        back_populates="brand",
    )
