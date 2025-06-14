from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.shared import Diametr


class Disc(Base):
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=False,
        index=True,
    )
