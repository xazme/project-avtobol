from uuid import UUID
from sqlalchemy import Select, Insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .order_item_model import OrderItem
from ..order import Order


class OrderItemRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: OrderItem,
    ):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: OrderItem = model

    async def create_order_items(
        self,
        list_of_orders_items: list[dict],
    ) -> OrderItem | None:
        stmt = Insert(self.model)
        try:
            await self.session.execute(statement=stmt, params=list_of_orders_items)
            await self.session.commit()
            return list_of_orders_items
        except IntegrityError:
            await self.session.rollback()
            return None

    async def get_user_ordered_product_ids(
        self,
        user_id: UUID,
    ) -> list[UUID]:
        stmt = Select(self.model.product_id).join(Order).where(Order.user_id == user_id)
        result = await self.session.execute(stmt)
        product_ids = result.scalars().all()
        return product_ids
