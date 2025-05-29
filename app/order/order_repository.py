from uuid import UUID
from sqlalchemy import Select, Result, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.shared import BaseCRUD
from app.car.product import Product
from .order_model import Order
from .order_enums import OrderStatuses


class OrderRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: Order,
    ):
        super().__init__(session=session, model=model)
        self.session = session
        self.model = model

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
            .options(
                selectinload(self.model.user),
                selectinload(self.model.product).joinedload(Product.car_brand),
                selectinload(self.model.product).joinedload(Product.car_series),
                selectinload(self.model.product).joinedload(Product.car_part),
            )
            .order_by(self.model.created_at)
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_all_orders(
        self,
        page,
        page_size,
        status: OrderStatuses,
    ):
        stmt = (
            Select(self.model)
            .options(
                selectinload(self.model.user),
                selectinload(self.model.product).joinedload(Product.car_brand),
                selectinload(self.model.product).joinedload(Product.car_series),
                selectinload(self.model.product).joinedload(Product.car_part),
            )
            .limit(limit=page_size)
            .offset((page - 1) * page_size)
            .order_by(self.model.created_at)
            .where(self.model.status == status)
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def change_order_status(
        self,
        order_id: UUID,
        status: OrderStatuses,
    ):
        order = await super().get_by_id(id=order_id)

        try:
            order.status = status
            await self.session.commit()
            await self.session.refresh(order)
            return order
        except IntegrityError:
            await self.session.rollback()
            return None

    async def create_orders(self, list_of_products: list):
        list_of_orders = [Order(**order_data) for order_data in list_of_products]
        try:
            self.session.add_all(list_of_orders)
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            return None
