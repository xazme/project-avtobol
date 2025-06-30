import uuid
from uuid import UUID
from typing import TYPE_CHECKING
from app.user import UserHandler
from app.cart import CartHandler
from app.car.product import ProductHandler
from app.shared import ExceptionRaiser
from .order_handler import OrderHandler
from .order_schema import OrderCreate, OrderCreatePrivate

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

    async def create_order(
        self,
        from_cart: bool,
        data: OrderCreate,
    ):
        user = await self.user_handler.repository.get_user_by_phone_number(
            phone_number=data.user_phone,
        )
        if user:
            result = await self.create_order_for_exist_user(
                from_cart=from_cart,
                user_id=user.id,
                data=data,
            )
            return result
        else:
            result = await self.create_order_for_guest(data=data)
            return result

    async def create_order_manually(
        self,
        data: OrderCreatePrivate,
    ) -> list["Order"]:
        order_data: dict = data.model_dump()

        articles: list = order_data.get("articles")
        user_phone = order_data.get("user_phone")

        if user_phone:
            user = await self.user_handler.repository.get_user_by_phone_number(
                phone_number=user_phone
            )

        order_data.pop("articles")

        products = [
            await self.product_handler.get_product_by_article(article=article)
            for article in articles
        ]

        user_orders: list = await self.order_handler.get_all_orders_by_phone_number(
            phone_number=user_phone
        )

        user_orders_id: list = [order.product.id for order in user_orders]

        updated_positions = []
        visited = set()
        order_group_id = uuid.uuid4()
        for product in products:
            if product.id not in user_orders_id and product.id not in visited:
                base_order = {
                    **order_data,
                    "product_id": product.id,
                    "order_group_id": order_group_id,
                }

                if user:
                    base_order.pop("user_name", None)
                    base_order.pop("user_phone", None)
                    base_order.update({"user_id": user.id})
                else:
                    base_order.update({"user_id": None})

                updated_positions.append(base_order)
                visited.add(product.id)

        if len(updated_positions) <= 0:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Заявки не были созданы.",
            )

        orders = await self.order_handler.repository.create_orders(
            list_of_products=updated_positions
        )
        if not orders:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Неудалось разместить заказ.",
            )

        return orders

    async def create_order_for_guest(self, data: OrderCreate) -> list["Order"]:
        product = await self.product_handler.get_product_by_article(
            article=data.article
        )

        order_data = data.model_dump(exclude_unset=True)

        base_order = {
            **order_data,
            "user_id": None,
            "product_id": product.id,
        }

        order = await self.order_handler.repository.create_orders(
            list_of_products=[base_order],
        )

        if not order:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail="Не удалось создать заказ.",
            )

        return order

    async def create_order_for_exist_user(
        self,
        user_id: UUID,
        from_cart: bool,
        data: OrderCreate,
    ) -> list["Order"]:

        order_data = data.model_dump(exclude_unset=True)
        order_data.pop("article")

        order_group_id = uuid.uuid4()
        updated_positions = []

        if from_cart:
            user_positions = await self.cart_handler.get_all_user_positions(
                user_id=user_id
            )
            if not user_positions:
                ExceptionRaiser.raise_exception(
                    status_code=400,
                    detail="Корзина пуста.",
                )

            visited = set()
            for position in user_positions:
                if position.product_id not in visited:
                    updated_positions.append(
                        {
                            **order_data,
                            "user_id": user_id,
                            "product_id": position.product_id,
                            "order_group_id": order_group_id,
                        }
                    )
                    visited.add(position.product_id)
        else:
            if not data.article:
                ExceptionRaiser.raise_exception(
                    status_code=400,
                    detail="Артикул не указан.",
                )

            product = await self.product_handler.get_product_by_article(
                article=data.article
            )

            base_order = {
                **order_data,
                "user_id": user_id,
                "product_id": product.id,
                "order_group_id": order_group_id,
            }
            base_order.pop("user_phone")
            base_order.pop("user_name")
            updated_positions.append(base_order)

        if not updated_positions:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Заявки не были созданы.",
            )

        orders = await self.order_handler.repository.create_orders(
            list_of_products=updated_positions,
        )
        if not orders:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail="Не удалось создать заказ.",
            )

        return orders

    def __build_order_payload(
        self,
        base_data: dict,
        user_id: UUID | None,
        product_id: UUID,
        order_group_id: UUID,
    ) -> dict:
        return {
            **base_data,
            "user_id": user_id,
            "product_id": product_id,
            "order_group_id": order_group_id,
        }
