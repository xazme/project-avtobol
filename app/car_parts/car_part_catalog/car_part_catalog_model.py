from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class CarPartCatalog(Base):
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
