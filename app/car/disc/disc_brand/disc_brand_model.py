from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from ..disc import Disc


class DiscBrand(Base):
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )
    discs: Mapped[list["Disc"]] = relationship(
        back_populates="brand",
    )
