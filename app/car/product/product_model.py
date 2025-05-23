from typing import TYPE_CHECKING
from app.database import Base
from sqlalchemy import String, Integer, Float, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.car.car_brand import CarBrand
    from app.car.car_series import CarSeries
    from app.car.car_part_catalog import CarPartCatalog
    from app.cart import Cart


class Product(Base):
    brand_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("carbrand.id"),
        nullable=False,
    )
    series_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("carseries.id"),
        nullable=False,
    )
    car_part_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("carpartcatalog.id"),
        nullable=False,
    )
    pictures: Mapped[list] = mapped_column(
        ARRAY(String),
        nullable=False,
        unique=True,
    )

    # relationships
    car_brand: Mapped["CarBrand"] = relationship(back_populates="car_part")
    car_series: Mapped["CarSeries"] = relationship(back_populates="car_part")
    car_part: Mapped["CarPartCatalog"] = relationship(back_populates="car_part")
    cart: Mapped[list["Cart"]] = relationship(back_populates="product")

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
