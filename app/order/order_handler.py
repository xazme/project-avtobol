from typing import TYPE_CHECKING, Optional
from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .order_repository import OrderRepository
from .order_model import Order
from .order_schema import OrderCreatePrivate
from .order_enums import OrderStatuses


class OrderHandler(BaseHandler):

    def __init__(self, repository: OrderRepository):
        super().__init__(repository)
        self.repository: OrderRepository = repository

    async def get_all_orders_by_user_id(
        self,
        user_id: UUID,
        status: OrderStatuses,
    ) -> list[Order]:
        return await self.repository.get_all_orders_by_user_id(
            user_id=user_id,
            status=status,
        )

    async def get_all_orders_by_phone_number(
        self,
        phone_number: str,
    ) -> list[Order]:
        return await self.repository.get_all_orders_by_phone_number(
            phone_number=phone_number,
        )

    async def change_order_status(
        self,
        order_id: UUID,
        status: OrderStatuses,
    ) -> Optional[Order]:
        upd_order = await self.repository.change_order_status(
            order_id=order_id,
            status=status,
        )
        if not upd_order:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Order not found or already closed.",
            )

        return upd_order

    async def get_all_orders_by_scroll(
        self,
        query: str,
        cursor: int | None,
        take: int | None,
        status: OrderStatuses,
    ) -> list[Order]:
        return await self.repository.get_all_orders_by_scroll(
            query=query,
            cursor=cursor,
            take=take,
            status=status,
        )
