from uuid import UUID
from typing import Optional
from app.shared import BaseHandler, ExceptionRaiser
from .order_repository import OrderRepository
from .order_enums import OrderStatuses
from .order_model import Order
from .order_schema import OrderFilters, OrderFiltersCompressed, OrderUpdate


class OrderHandler(BaseHandler):

    def __init__(self, repository: OrderRepository):
        super().__init__(repository)
        self.repository: OrderRepository = repository

    async def update_order(
        self,
        order_id: UUID,
        data: OrderUpdate,
    ) -> Optional["Order"]:
        updated_order = await self.repository.update_by_id(
            id=order_id,
            data=data.model_dump(exclude_unset=True),
        )
        if not updated_order:
            ExceptionRaiser.raise_exception(
                status_code=422,
                detail=f"Не удалось обновить заказ.",
            )
        return updated_order

    async def update_order_status(
        self,
        order_id: UUID,
        new_status: OrderStatuses,
    ) -> Optional["Order"]:
        order: "Order" | None = await self.repository.update_order_status(
            order_id=order_id,
            new_status=new_status,
        )

        if not order:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Заказ {order_id} не найден.",
            )
        return order

    async def get_all_orders(
        self,
        cursor: int | None,
        take: int | None,
        filters: OrderFilters,
    ) -> tuple[int | None, list["Order"]]:
        return await self.repository.get_orders_by_scroll(
            cursor=cursor,
            take=take,
            filters=filters,
        )

    async def get_user_orders(
        self,
        user_id: UUID,
        cursor: int | None,
        take: int | None,
        filters: OrderFiltersCompressed,
    ) -> tuple[int | None, list["Order"]]:
        return await self.repository.get_user_orders_by_scroll(
            user_id=user_id,
            cursor=cursor,
            take=take,
            filters=filters,
        )
