# from typing import TYPE_CHECKING
# from datetime import datetime
# from sqlalchemy import String, Integer, DateTime, ForeignKey, func, Enum as SqlEnum
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from app.database import Base
# from app.shared import OrderStatuses

# if TYPE_CHECKING:
#     from app.user import User
#     from app.car.product import Product


# class Order(Base):
#     user_id: Mapped[int] = mapped_column(
#         Integer,
#         ForeignKey(
#             "user.id",
#             ondelete="CASCADE",
#         ),
#         nullable=False,
#         index=True,
#     )
#     product_id: Mapped[int] = mapped_column(
#         Integer,
#         ForeignKey(
#             "product.id",
#             ondelete="CASCADE",
#         ),
#         nullable=False,
#         index=True,
#     )
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime,
#         server_default=func.now(),
#     )
#     description: Mapped[str] = mapped_column(
#         String,
#         nullable=True,
#     )
#     status: Mapped[SqlEnum] = mapped_column(
#         SqlEnum(OrderStatuses),
#         nullable=False,
#         default=OrderStatuses.OPEN,
#     )

#     # relationships
#     product: Mapped["Product"] = relationship(
#         back_populates="order",
#         cascade="all, delete-orphan",
#     )
#     user: Mapped["User"] = relationship(
#         back_populates="order",
#         cascade="all, delete-orphan",
#     )
