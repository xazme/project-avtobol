from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import String, DateTime, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.shared import Roles, Statuses

if TYPE_CHECKING:
    from app.token import Token
    from app.bucket import Bucket


class User(Base):
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
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
        SqlEnum(Statuses),
        nullable=False,
        default=Statuses.ACTIVE,
    )
    role: Mapped[SqlEnum] = mapped_column(
        SqlEnum(Roles),
        nullable=False,
        default=Roles.CLIENT,
    )

    # relationships
    token: Mapped["Token"] = relationship(back_populates="user")
    bucket: Mapped["Bucket"] = relationship(back_populates="user")
