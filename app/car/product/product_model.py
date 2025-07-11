from typing import TYPE_CHECKING
from uuid import UUID
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
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.shared import generate_article
from .product_enums import (
    ProductCondition,
    Availability,
    Currency,
    BodyType,
)

if TYPE_CHECKING:
    from ..car_brand import CarBrand
    from ..car_series import CarSeries
    from ..car_part import CarPart
    from ..disc import Disc
    from ..tire import Tire
    from ..engine import Engine
    from app.cart import CartItem
    from app.order import OrderItem
    from app.user import User


class Product(Base):
    article: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
        default=generate_article,
    )

    OEM: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    car_brand_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "carbrand.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
        index=True,
    )

    car_series_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "carseries.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
        index=True,
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

    car_part_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "carpart.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
        index=True,
    )

    VIN: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    type_of_body: Mapped[BodyType | None] = mapped_column(
        SqlEnum(BodyType),
        nullable=True,
    )

    description: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    discount: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    currency: Mapped[Currency] = mapped_column(
        SqlEnum(Currency),
        default=Currency.USD,
        nullable=False,
    )

    condition: Mapped[ProductCondition] = mapped_column(
        SqlEnum(ProductCondition),
        default=ProductCondition.USED,
    )

    availability: Mapped[Availability] = mapped_column(
        SqlEnum(Availability),
        default=Availability.IN_STOCK,
        index=True,
    )

    note: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    count: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        index=True,
    )

    is_printed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        index=True,
    )

    pictures: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
    )

    post_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    allegro_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        index=True,
    )

    idriver_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        index=True,
    )

    car_brand: Mapped["CarBrand"] = relationship(
        back_populates="products",
    )
    car_series: Mapped["CarSeries"] = relationship(
        back_populates="products",
    )
    car_part: Mapped["CarPart"] = relationship(
        back_populates="products",
    )
    tire: Mapped["Tire"] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        uselist=False,
    )
    disc: Mapped["Disc"] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        uselist=False,
    )
    engine: Mapped["Engine"] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        uselist=False,
    )
    user: Mapped["User"] = relationship(
        back_populates="product",
    )
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product",
    )
    cart_items: Mapped[list["CartItem"]] = relationship(
        back_populates="product",
    )
