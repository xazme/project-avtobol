from typing import TYPE_CHECKING
from app.database import Base
from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.car_parts.car_brand import CarBrand
    from app.car_parts.car_series import CarSeries
    from app.car_parts.car_part_catalog import CarPartCatalog


class CarBrandPartSeriesAssoc(Base):
    brand_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("carbrand.id"),
        nullable=False,
    )
    car_part_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("carpartcatalog.id"),
        nullable=False,
    )
    series_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("carseries.id"),
        nullable=False,
    )

    # relationships
    brand: Mapped["CarBrand"] = relationship(back_populates="car_part")
    car_part: Mapped["CarPartCatalog"] = relationship(back_populates="car_part")
    series: Mapped["CarSeries"] = relationship(back_populates="car_part")

    # year: Mapped[int] = mapped_column(
    #     Integer,
    #     nullable=True,
    # )
    # type_of_body: Mapped[str] = mapped_column(
    #     String,
    #     nullable=True,
    # )
    # volume: Mapped[float] = mapped_column(
    #     Float,
    #     nullable=True,
    # )
    # gearbox: Mapped[str] = mapped_column(
    #     String,
    #     nullable=True,
    # )
    # fuel: Mapped[str] = mapped_column(
    #     String,
    #     nullable=True,
    # )
    # type_of_engine: Mapped[str] = mapped_column(
    #     String,
    #     nullable=True,
    # )
    # VIN: Mapped[int] = mapped_column(
    #     Integer,
    #     nullable=True,
    # )
    # oem: Mapped[int] = mapped_column(
    #     Integer,
    #     nullable=True,
    # )
    # note: Mapped[str] = mapped_column(
    #     String,
    #     nullable=True,
    # )
    # description: Mapped[str] = mapped_column(
    #     String,
    #     nullable=True,
    # )
    # real_price: Mapped[float] = mapped_column(
    #     Float,
    #     nullable=False,
    # )
    # fake_price: Mapped[float] = mapped_column(
    #     Float,
    #     nullable=False,
    # )
    # count: Mapped[int] = mapped_column(
    #     Integer,
    #     nullable=False,
    #     default=0,
    # )
    # condition: Mapped[str] = mapped_column(
    #     String,
    #     nullable=False,
    #     default=1,
    # )
