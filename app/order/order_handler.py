from typing import TYPE_CHECKING
from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .order_repository import OrderRepository
from .order_enums import OrderStatuses
from .order_schema import OrderCreate

if TYPE_CHECKING:
    from app.cart import Cart


class OrderHandler(BaseHandler):
    def __init__(
        self,
        repository,
    ):
        super().__init__(repository)
        self.repository: OrderRepository = repository

    async def get_all_orders_by_user_id(
        self,
        user_id: UUID,
        status: OrderStatuses,
    ):
        return await self.repository.get_all_orders_by_user_id(
            user_id=user_id,
            status=status,
        )

    async def create_order(
        self,
        user_id: int,
        user_positions: list["Cart"],
        data: OrderCreate,
    ):

        updated_positions = [
            data.model_copy(
                update={
                    "user_id": position.user_id,
                    "product_id": position.product_id,
                }
            )
            for position in user_positions
        ]

        positions_in_order = await self.create_obj(updated_positions)
        if not positions_in_order:
            ExceptionRaiser.raise_exception(status_code=500)
        return positions_in_order
