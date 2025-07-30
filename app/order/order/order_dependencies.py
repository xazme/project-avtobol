from typing import TYPE_CHECKING
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.car.product import get_product_handler
from app.cart.cart import get_cart_handler
from app.cart.cart_items import get_cart_item_handler
from app.database import DBService
from .order_handler import OrderHandler
from .order_model import Order
from .order_repository import OrderRepository
from .order_orchestrator import OrderOrchestrator
from ..order_item import get_order_item_handler

if TYPE_CHECKING:

    from app.car.product import ProductHandler
    from app.cart.cart import CartHandler
    from app.cart.cart_items import CartItemHandler
    from .order_handler import OrderHandler
    from ..order_item import OrderItemHandler


def get_order_handler(
    session: AsyncSession = Depends(DBService.get_session),
):
    repository = OrderRepository(
        session=session,
        model=Order,
    )
    return OrderHandler(repository=repository)


def get_order_orchestrator(
    cart_handler: "CartHandler" = Depends(get_cart_handler),
    order_handler: "OrderHandler" = Depends(get_order_handler),
    cart_item_handler: "CartItemHandler" = Depends(get_cart_item_handler),
    order_item_handler: "OrderItemHandler" = Depends(get_order_item_handler),
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    return OrderOrchestrator(
        cart_handler=cart_handler,
        cart_item_handler=cart_item_handler,
        order_handler=order_handler,
        order_item_handler=order_item_handler,
        product_handler=product_handler,
    )
