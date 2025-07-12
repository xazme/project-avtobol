from typing import Optional
from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .order_item_repository import OrderItemRepository
from .order_item_enums import OrderItemStatus
from .order_item_model import OrderItem


class OrderItemHandler(BaseHandler):

    def __init__(self, repository: OrderItemRepository):
        super().__init__(repository)
        self.repository: OrderItemRepository = repository

    async def get_order_items_by_order_id(
        self,
        order_id: UUID,
    ) -> list[OrderItem]:
        return await self.repository.get_order_items_by_order_id(
            order_id=order_id,
        )

    async def update_order_item_status(
        self,
        order_item_id: UUID,
        new_status: OrderItemStatus,
    ) -> Optional[OrderItem]:
        order_item: "OrderItem" | None = await self.repository.update_order_item_status(
            order_item_id=order_item_id,
            new_status=new_status,
        )

        if not order_item:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Заказ {order_item_id} не найден.",
            )
        return order_item
