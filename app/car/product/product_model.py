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
from app.shared import Diametr
from app.car.tire import Season, CarType
from .product_enums import (
    ProductCondition,
    FuelType,
    BodyType,
    GearboxType,
    Availability,
    Currency,
)

if TYPE_CHECKING:
    from app.car.tire import Tire
    from app.car.disc import Disc
    from app.car.car_brand import CarBrand
    from app.car.car_series import CarSeries
    from app.car.car_part_catalog import CarPart
    from app.cart import Cart
    from app.order import Order


class Product(Base):
    # Обязательные связи
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
            "carpart.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # Шины и диски (бренды)
    tire_brand_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "tire.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=True,
        index=True,
    )
    disc_brand_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "disc.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=True,
        index=True,
    )

    # Фото
    pictures: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
    )

    # Статусы
    is_available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    is_printed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    # Общие характеристики
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    OEM: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1885,
    )
    type_of_body: Mapped[BodyType | None] = mapped_column(
        SqlEnum(BodyType),
        nullable=True,
    )
    volume: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    gearbox: Mapped[GearboxType | None] = mapped_column(
        SqlEnum(GearboxType),
        nullable=True,
    )
    fuel: Mapped[FuelType | None] = mapped_column(
        SqlEnum(FuelType),
        nullable=True,
    )
    engine_type: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    VIN: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    # Диск
    disc_diametr: Mapped[Diametr | None] = mapped_column(
        SqlEnum(Diametr),
        nullable=True,
    )
    disc_width: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    disc_ejection: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    disc_dia: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    disc_holes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    disc_pcd: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    disc_model: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    # Шины
    tires_diametr: Mapped[Diametr | None] = mapped_column(
        SqlEnum(Diametr),
        nullable=True,
    )
    tires_width: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    tires_height: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    tires_index: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    tires_car_type: Mapped[CarType | None] = mapped_column(
        SqlEnum(CarType),
        nullable=True,
    )
    tires_model: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    tires_season: Mapped[Season | None] = mapped_column(
        SqlEnum(Season),
        nullable=True,
    )
    tires_residue: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # Основное
    description: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    discount: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    currency: Mapped[Currency] = mapped_column(
        SqlEnum(Currency),
        nullable=False,
        default=Currency.USD,
    )
    condition: Mapped[ProductCondition] = mapped_column(
        SqlEnum(ProductCondition),
        nullable=False,
        default=ProductCondition.USED,
    )
    availability: Mapped[Availability] = mapped_column(
        SqlEnum(Availability),
        nullable=False,
        default=Availability.IN_STOCK,
    )
    note: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    # idriver_id: Mapped[int] = mapped_column(
    #     Integer,
    #     index=True,
    #     nullable=True,
    # )

    # allegro_id:Mapped[int] = mapped_colu

    # relationships
    car_brand: Mapped["CarBrand"] = relationship(
        back_populates="product",
    )
    car_series: Mapped["CarSeries"] = relationship(
        back_populates="product",
    )
    car_part: Mapped["CarPart"] = relationship(
        back_populates="product",
    )
    tire: Mapped["Tire"] = relationship(
        back_populates="product",
    )
    disc: Mapped["Disc"] = relationship(
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
