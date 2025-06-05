from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import String, DateTime, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from .user_enums import UserRoles, UserStatuses

if TYPE_CHECKING:
    from app.token import Token
    from app.cart import Cart
    from app.order import Order


class User(Base):
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )
    phone_number: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )
    password: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    status: Mapped[SqlEnum] = mapped_column(
        SqlEnum(UserStatuses),
        nullable=False,
        default=UserStatuses.ACTIVE,
    )
    role: Mapped[SqlEnum] = mapped_column(
        SqlEnum(UserRoles),
        nullable=False,
        default=UserRoles.CLIENT,
    )

    # relationships
    token: Mapped["Token"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    cart: Mapped[list["Cart"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    order: Mapped[list["Order"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
