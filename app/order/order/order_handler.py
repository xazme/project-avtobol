from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .order_repository import OrderRepository
from .order_enums import OrderStatuses
from .order_model import Order


class OrderHandler(BaseHandler):

    def __init__(self, repository: OrderRepository):
        super().__init__(repository)
        self.repository: OrderRepository = repository

    async def update_order_status(
        self,
        order_id: UUID,
        new_status: OrderStatuses,
    ):
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
