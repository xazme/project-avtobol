from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, ARRAY
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.user import User


class Cart(Base):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
        nullable=False,
        index=True,
    )
    items: Mapped[list] = mapped_column(
        ARRAY,
    )

    # relationship
    user: Mapped["User"] = relationship(back_populates="bucket")
