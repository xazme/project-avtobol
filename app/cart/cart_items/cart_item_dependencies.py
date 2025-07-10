from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from app.car.product import ProductHandler, get_product_handler
from .cart_item_orchestrator import CartItemOrchestrator
from .cart_item_model import CartItem
from .cart_item_handler import CartItemHandler
from .cart_item_repository import CartItemRepository
from ..cart import CartHandler, get_cart_handler


def get_cart_items_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> CartItemHandler:
    repository = CartItemRepository(
        session=session,
        model=CartItem,
    )
    return CartItemHandler(repository=repository)


def get_cart_item_orchestrator(
    product_handler: ProductHandler = Depends(get_product_handler),
    cart_handler: CartHandler = Depends(get_cart_handler),
    cart_item_handler: CartItemHandler = Depends(get_cart_items_handler),
):
    return CartItemOrchestrator(
        product_handler=product_handler,
        cart_handler=cart_handler,
        cart_item_handler=cart_item_handler,
    )
