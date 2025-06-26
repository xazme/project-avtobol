from typing import TYPE_CHECKING, Optional
from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .order_repository import OrderRepository
from .order_model import Order
from .order_enums import OrderStatuses
from .order_schema import OrderCreate

if TYPE_CHECKING:
    from app.cart import Cart


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

    async def create_order(
        self,
        user_positions: list["Cart"],
        data: OrderCreate,
    ) -> list[Order]:
        if not user_positions:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Cart is empty, nothing to process.",
            )

        order_data = data.model_dump(exclude_unset=True)

        updated_positions = [
            {
                **order_data,
                "user_id": position.user_id,
                "product_id": position.product_id,
            }
            for position in user_positions
        ]

        positions_in_order = await self.repository.create_orders(
            list_of_products=updated_positions,
        )

        if not positions_in_order:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail="Failed to create order, please try again later.",
            )

        return positions_in_order
