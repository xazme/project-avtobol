from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .order_item_model import OrderItem
from .order_item_handler import OrderItemHandler
from .order_item_repository import OrderItemRepository


def get_order_item_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> OrderItemHandler:
    repository = OrderItemRepository(
        session=session,
        model=OrderItem,
    )
    return OrderItemHandler(repository=repository)
