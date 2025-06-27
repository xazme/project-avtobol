from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from app.user import UserHandler, get_user_handler
from app.cart import CartHandler, get_cart_handler
from app.car.product import ProductHandler, get_product_handler
from .order_handler import OrderHandler
from .order_model import Order
from .order_repository import OrderRepository
from .order_orchestrator import OrderOrchestrator


def get_order_handler(
    session: AsyncSession = Depends(DBService.get_session),
):
    repository = OrderRepository(session=session, model=Order)
    return OrderHandler(repository=repository)


def get_order_orchestrator(
    user_handler: UserHandler = Depends(get_user_handler),
    cart_handler: CartHandler = Depends(get_cart_handler),
    order_handler: OrderHandler = Depends(get_order_handler),
    product_handler: ProductHandler = Depends(get_product_handler),
):
    return OrderOrchestrator(
        user_handler=user_handler,
        cart_handler=cart_handler,
        order_handler=order_handler,
        product_handler=product_handler,
    )
