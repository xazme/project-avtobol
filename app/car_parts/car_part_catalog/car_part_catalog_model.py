from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.car_parts.car_brand_series_assoc import CarBrandPartSeriesAssoc


class CarPartCatalog(Base):
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    car_part: Mapped["CarBrandPartSeriesAssoc"] = relationship(
        back_populates="car_part",
    )
