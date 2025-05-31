from typing import TYPE_CHECKING
from datetime import datetime
from app.database import Base
from sqlalchemy import (
    func,
    String,
    Integer,
    Float,
    ForeignKey,
    ARRAY,
    DateTime,
    Boolean,
    Enum as SqlEnum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .product_enums import ProductCondition, FuelType, BodyType, GearboxType

if TYPE_CHECKING:
    from app.car.car_brand import CarBrand
    from app.car.car_series import CarSeries
    from app.car.car_part_catalog import CarPartCatalog
    from app.cart import Cart
    from app.order import Order


class Product(Base):
    car_brand_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "carbrand.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        index=True,
    )
    car_series_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "carseries.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        index=True,
    )
    car_part_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "carpartcatalog.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        index=True,
    )
    pictures: Mapped[list] = mapped_column(
        ARRAY(String),
        nullable=False,
        unique=False,
    )
    is_available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    year: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    type_of_body: Mapped[SqlEnum] = mapped_column(
        SqlEnum(BodyType),
        nullable=True,
        default=None,
    )
    volume: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    gearbox: Mapped[SqlEnum] = mapped_column(
        SqlEnum(GearboxType),
        nullable=True,
        default=None,
    )
    fuel: Mapped[SqlEnum] = mapped_column(
        SqlEnum(FuelType),
        nullable=True,
        default=None,
    )
    type_of_engine: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    VIN: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    oem: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    note: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    real_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    fake_price: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    condition: Mapped[SqlEnum] = mapped_column(
        SqlEnum(ProductCondition),
        nullable=False,
    )

    # relationships
    car_brand: Mapped["CarBrand"] = relationship(
        back_populates="product",
    )
    car_series: Mapped["CarSeries"] = relationship(
        back_populates="product",
    )
    car_part: Mapped["CarPartCatalog"] = relationship(
        back_populates="product",
    )
    cart: Mapped[list["Cart"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )
    order: Mapped[list["Order"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )
