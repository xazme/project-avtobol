from datetime import datetime
from sqlalchemy import func
from sqlalchemy import String, DateTime, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.shared import Roles, Statuses


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
        index=True,
    )
    password: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=False,
        index=True,
    )
    last_activity: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    status: Mapped[SqlEnum] = mapped_column(
        SqlEnum(Statuses),
        nullable=False,
        default=Statuses.OFFLINE,
    )
    role: Mapped[SqlEnum] = mapped_column(
        SqlEnum(Roles),
        nullable=False,
        default=Roles.WORKER,
    )
