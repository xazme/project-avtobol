from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from ..tire import Tire


class TireBrand(Base):
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=False,
        index=True,
    )
    tires: Mapped[list["Tire"]] = relationship(
        back_populates="brand",
    )
