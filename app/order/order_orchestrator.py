from uuid import UUID
from typing import TYPE_CHECKING
from app.user import UserHandler
from app.cart import CartHandler
from app.car.product import ProductHandler
from app.shared import ExceptionRaiser
from .order_handler import OrderHandler
from .order_schema import OrderCreate

if TYPE_CHECKING:
    from app.order import Order


class OrderOrchestrator:

    def __init__(
        self,
        user_handler: UserHandler,
        cart_handler: CartHandler,
        order_handler: OrderHandler,
        product_handler: ProductHandler,
    ):
        self.user_handler: UserHandler = user_handler
        self.cart_handler: CartHandler = cart_handler
        self.order_handler: OrderHandler = order_handler
        self.product_handler: ProductHandler = product_handler

    async def create_order(self, data: OrderCreate):
        user = await self.user_handler.repository.get_user_by_phone_number(
            phone_number=data.user_phone,
        )
        if user:
            result = await self.create_order_for_exist_user(
                user_id=user.id,
                data=data,
            )
            return result
        else:
            result = await self.create_order_for_guest(data=data)
            return result

    async def create_order_for_exist_user(
        self,
        user_id: UUID,
        data: OrderCreate,
    ) -> list["Order"]:

        user_positions = await self.cart_handler.get_all_user_positions(user_id=user_id)

        if not user_positions:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Корзина пуста. Удалять нечего",
            )

        order_data = data.model_dump(exclude_unset=True)
        order_data.pop("article")
        updated_positions = [
            {
                **order_data,
                "user_id": position.user_id,
                "product_id": position.product_id,
            }
            for position in user_positions
        ]

        orders = await self.order_handler.repository.create_orders(
            list_of_products=updated_positions,
        )

        if not orders:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail="Неудалось создать заказ.",
            )

        return orders

    async def create_order_for_guest(self, data: OrderCreate) -> list["Order"]:
        product = await self.product_handler.get_product_by_article(
            article=data.article
        )

        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Товар c указанным артикулом не найден.",
            )

        order_data = data.model_dump(exclude_unset=True)
        order_data.pop("article")
        guest_order = {
            **order_data,
            "user_id": None,
            "product_id": product.id,
        }

        order = await self.order_handler.repository.create_orders(
            list_of_products=[guest_order],
        )

        if not order:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail="Не удалось создать заказ.",
            )

        return order
