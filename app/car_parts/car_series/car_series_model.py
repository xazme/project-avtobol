from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from app.database import Base

if TYPE_CHECKING:
    from app.car_parts.car_brand import CarBrand


class CarSeries(Base):
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
    )
    year: Mapped[str] = mapped_column(String)

    brand_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("carbrand.id"),
        index=True,
        unique=False,
    )

    # relationship
    brand: Mapped["CarBrand"] = relationship(
        back_populates="series",
    )
