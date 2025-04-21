from typing import TYPE_CHECKING
from app.database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    pass


class CarPart(Base):
    pass
    # article: Mapped[str] = mapped_column()
    # part_id:Mapped[str] = mapped_column(ForeignKey("carpart.id"))
    # brand_id:Mapped[]
    # series_id:Mapped[]
    # year:Mapped[str]
    # type_of_body:Mapped[str] = mapped_column(nullable=False)
    # volume:Mapped[float]
    # gearbox:Mapped[]
    # type_of_engine:Mapped[]
    # VIN:Mapped[] = mapped_column()
    # oem:Mapped[] = mapped_column(nullable=True)
    # note:Mapped[]
    # description:Mapped[]
    # real_price:Mapped[]
    # fake_price:Mapped
    # count:Mapped[int]
