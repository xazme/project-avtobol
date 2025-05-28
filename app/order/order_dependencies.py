from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .order_handler import OrderHandler
from .order_model import Order
from .order_repository import OrderRepository


def get_order_handler(
    session: AsyncSession = Depends(DBService.get_session),
):
    repository = OrderRepository(session=session, model=Order)
    return OrderHandler(repository=repository)
