from typing import TYPE_CHECKING
from uuid import UUID
from app.shared import ExceptionRaiser
from app.cart.cart_items import CartItem
from .order_schema import OrderCreate

if TYPE_CHECKING:

    from app.car.product import ProductHandler, Product
    from app.cart.cart import CartHandler, Cart
    from app.cart.cart_items import CartItemHandler, CartItem
    from .order_model import Order
    from .order_handler import OrderHandler
    from ..order_items import OrderItemHandler


class OrderOrchestrator:
    def __init__(
        self,
        # user_handler: "UserHandler",
        cart_handler: "CartHandler",
        order_handler: "OrderHandler",
        order_item_handler: "OrderItemHandler",
        cart_item_handler: "CartItemHandler",
        product_handler: "ProductHandler",
    ):
        # self.user_handler: "UserHandler" = user_handler
        self.cart_handler: "CartHandler" = cart_handler
        self.order_handler: "OrderHandler" = order_handler
        self.cart_item_handler: "CartItemHandler" = cart_item_handler
        self.order_item_handler: OrderItemHandler = order_item_handler
        self.product_handler: "ProductHandler" = product_handler

    async def create_order_manually(
        self,
        data: OrderCreate,
        product_articles: list[str],
    ):
        order: "Order" = await self.order_handler.create_obj(data=data)
        order_id = order.id

        

    async def create_order(
        self,
        user_id: UUID,
        data: OrderCreate,
    ):
        user: "Cart" = await self.get_user_cart_id(user_id=user_id)
        order_data = data.model_dump(exclude_unset=True)
        order_data.update({"user_id": user.id})

        order: "Order" = await self.order_handler.create_obj(data=order_data)
        order_id = order.id

        user_ordered_products_ids: list[UUID] = (
            await self.order_item_handler.repository.get_user_ordered_product_ids(
                user_id=user_id
            )
        )

        user_cart_items: list["CartItem"] = await self.get_user_cart(user_id=user_id)

        order_items = []
        for item in user_cart_items:
            if item.product_id in user_ordered_products_ids:
                continue

            order_item_data = {
                "order_id": order_id,
                "product_id": item.product_id,
            }

            order_items.append(order_item_data)

        await self.order_item_handler.repository.create_order_items(
            list_of_orders_items=order_items,
        )

    async def get_user_cart(
        self,
        user_id: UUID,
    ):
        user_cart_id = await self.get_user_cart_id(user_id=user_id)
        user_cart: list[CartItem] = (
            await self.cart_item_handler.repository.get_all_user_positions(
                cart_id=user_cart_id
            )
        )
        return user_cart

    async def get_user_cart_id(
        self,
        user_id: UUID,
    ) -> UUID:
        user_cart: Cart | None = await self.cart_handler.repository.get_user_cart(
            user_id=user_id,
        )
        if not user_cart:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="У пользователя отсутствует корзина. Вероятнее всего пользователя несуществует. ",
            )
        user_cart_id = user_cart.id
        return user_cart_id
