from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from app.cart import get_cart_handler
from .order_handler import OrderHandler
from .order_model import Order
from .order_repository import OrderRepository


def get_order_handler(
    session: AsyncSession = Depends(DBService.get_session),
    cart_handler=Depends(get_cart_handler),
):
    repository = OrderRepository(session=session, model=Order)
    return OrderHandler(repository=repository, cart_handler=cart_handler)
