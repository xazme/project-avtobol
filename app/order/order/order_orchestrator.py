import copy
from typing import TYPE_CHECKING, Optional
from uuid import UUID
from app.shared import ExceptionRaiser
from app.cart.cart_items import CartItem
from .order_schema import OrderCreate, OrderFilters
from .order_enums import OrderStatuses
from ..order_item.order_item_enums import OrderItemStatus

if TYPE_CHECKING:

    from app.car.product import ProductHandler, Product
    from app.cart.cart import CartHandler, Cart
    from app.cart.cart_items import CartItemHandler, CartItem
    from .order_model import Order
    from .order_handler import OrderHandler
    from ..order_item import OrderItemHandler, OrderItem


class OrderOrchestrator:
    def __init__(
        self,
        cart_handler: "CartHandler",
        order_handler: "OrderHandler",
        order_item_handler: "OrderItemHandler",
        cart_item_handler: "CartItemHandler",
        product_handler: "ProductHandler",
    ):
        self.cart_handler: "CartHandler" = cart_handler
        self.order_handler: "OrderHandler" = order_handler
        self.cart_item_handler: "CartItemHandler" = cart_item_handler
        self.order_item_handler: "OrderItemHandler" = order_item_handler
        self.product_handler: "ProductHandler" = product_handler

    async def create_order_manually(
        self,
        data: OrderCreate,
        product_ids: list[UUID],
    ) -> "Order":
        if not product_ids:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Список продуктов пуст — невозможно создать заказ.",
            )

        order: "Order" = await self.order_handler.create_obj(data=data)
        order_id = order.id

        products: list["Product"] = (
            await self.product_handler.repository.get_products_by_ids(
                list_of_product_ids=product_ids,
            )
        )
        denied = []
        product_id_in_order = []
        order_items = []

        for product in products:
            if product.is_available != True:
                denied.append(product.article)
                continue
            order_item_data = {
                "order_id": order_id,
                "product_id": product.id,
            }
            order_items.append(order_item_data)
            product_id_in_order.append(product.id)

        if len(order_items) < 1:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail="Неудалось создать заказ. Количество позиций в ордере меньне единицы. Возможные причины: 1) Дубликаты в артикулах 2) Введенный артикул неверный 3) Товар недоступен",
            )

        await self.order_item_handler.repository.create_order_items(
            list_of_orders_items=order_items,
        )
        await self.product_handler.bulk_update_availability(
            products_id=product_id_in_order,
            new_status=False,
        )
        refreshed_order = await self.order_handler.get_obj_by_id(id=order_id)
        return refreshed_order, denied

    async def create_order(
        self,
        user_id: UUID,
        data: OrderCreate,
    ) -> "Order":
        user_cart_id: UUID | None = (
            await self.cart_handler.repository.get_user_cart_id_by_user_id(
                user_id=user_id,
            )
        )

        if not user_cart_id:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="У пользователя отсутствует корзина. Вероятнее всего он не существует, либо был удалён.",
            )

        order_data = data.model_dump(exclude_unset=True)
        order_data.update({"user_id": user_id})

        order: "Order" = await self.order_handler.create_obj(data=order_data)
        order_id = order.id

        user_ordered_products_ids_set = set(
            await self.order_item_handler.repository.get_user_ordered_product_ids(
                user_id=user_id
            )
        )

        user_cart_items: list["CartItem"] = await self.get_user_cart_items(
            user_id=user_id
        )

        product_ids_to_add = [
            item.product_id
            for item in user_cart_items
            if item.product_id not in user_ordered_products_ids_set
        ]

        if not product_ids_to_add:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail="Ни один товар из корзины не был добавлен в заказ. Все позиции уже были использованы ранее.",
            )

        products: list["Product"] = (
            await self.product_handler.repository.get_products_by_ids(
                list_of_product_ids=product_ids_to_add
            )
        )

        denied = []
        order_items = []
        product_ids_confirmed = []

        for product in products:
            if product.is_available != True:
                denied.append(product.article)
                continue

            order_items.append(
                {
                    "order_id": order_id,
                    "product_id": product.id,
                }
            )
            product_ids_confirmed.append(product.id)

        if not order_items:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail="Ни один товар не добавлен. Все товары недоступны или уже заказаны.",
            )

        await self.order_item_handler.repository.create_order_items(
            list_of_orders_items=order_items,
        )

        await self.product_handler.bulk_update_availability(
            products_id=product_ids_confirmed,
            new_status=False,
        )

        await self.cart_item_handler.repository.clear_user_cart(cart_id=user_cart_id)

        refreshed_order = await self.order_handler.get_obj_by_id(id=order_id)
        return refreshed_order, denied

    async def get_user_cart_items(
        self,
        user_id: UUID,
    ) -> list["CartItem"]:
        user_cart_id: UUID = await self.cart_handler.get_user_cart_id(user_id=user_id)
        user_cart: list["CartItem"] = (
            await self.cart_item_handler.repository.get_all_user_positions(
                cart_id=user_cart_id
            )
        )
        return user_cart

    async def update_order_status(
        self,
        order_id: UUID,
        new_status: OrderStatuses,
    ) -> Optional["Order"]:
        updated_order: "Order" = await self.order_handler.update_order_status(
            order_id=order_id, new_status=new_status
        )
        return updated_order

    async def update_order_item_status(
        self,
        order_item_id: UUID,
        new_status: OrderStatuses,
    ) -> Optional["OrderItem"]:
        updated_order_items: "OrderItem" = (
            await self.order_item_handler.update_order_item_status(
                order_item_id=order_item_id,
                new_status=new_status,
            )
        )
        do_restore: bool = self.__should_respore_product_availability(
            item_status=new_status,
        )

        if do_restore:
            await self.product_handler.update_product_availability(
                product_id=updated_order_items.product_id,
            )

        return updated_order_items

    def __should_respore_product_availability(
        self,
        item_status: OrderItemStatus,
    ) -> bool:
        restore_statuses = {
            OrderItemStatus.RETURNED,
            OrderItemStatus.CANCELLED,
            OrderItemStatus.REFUNDED,
            OrderItemStatus.OUT_OF_STOCK,
            OrderItemStatus.DENIED,
        }

        if item_status in restore_statuses:
            return True
        return False
