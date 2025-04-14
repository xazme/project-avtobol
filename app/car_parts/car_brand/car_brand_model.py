from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.car_parts.car_series import CarSeries


class CarBrand(Base):
    title: Mapped[str] = mapped_column(String)
    serie: Mapped[List["CarSeries"]] = relationship(back_populates="brand")
