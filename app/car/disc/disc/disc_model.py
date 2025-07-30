from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, Float, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.car.shared import Diametr

if TYPE_CHECKING:
    from app.car.product import Product
    from ..disc_brand import DiscBrand


class Disc(Base):
    disc_brand_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "discbrand.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "product.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )
    diametr: Mapped[Diametr] = mapped_column(
        SqlEnum(Diametr),
        nullable=True,
    )
    width: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    ejection: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    dia: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    holes: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    pcd: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    model: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    brand: Mapped["DiscBrand"] = relationship(
        back_populates="discs",
    )
    product: Mapped["Product"] = relationship(
        back_populates="disc",
    )
