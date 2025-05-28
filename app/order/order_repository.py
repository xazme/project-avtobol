from uuid import UUID
from sqlalchemy import Select, Result, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.shared import BaseCRUD
from .order_model import Order
from .order_enums import OrderStatuses


class OrderRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: Order,
    ):
        super().__init__(session, model)

    async def get_all_orders_by_user_id(
        self,
        user_id: UUID,
        status: OrderStatuses,
    ):
        stmt = (
            Select(self.model)
            .where(
                and_(
                    self.model.user_id == user_id,
                    self.model.status == status,
                )
            )
            .order_by(self.model.created_at)
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def create_orders(self, list_of_products: list):
        try:
            self.session.add_all(list_of_products)
            await self.session.commit()
            return list_of_products
        except IntegrityError:
            await self.session.rollback()
            return None
