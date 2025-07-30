from uuid import UUID
from sqlalchemy import Select, Insert, Result
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from app.car.product import Product
from .order_item_model import OrderItem
from .order_item_enums import OrderItemStatus
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

    async def get_order_items_by_order_id(
        self,
        order_id: UUID,
    ):
        stmt = (
            Select(self.model)
            .where(self.model.order_id == order_id)
            .options(
                selectinload(self.model.product).options(
                    selectinload(Product.car_brand),
                    selectinload(Product.car_series),
                    selectinload(Product.car_part),
                )
            )
        )
        result: Result = await self.session.execute(stmt)
        orders = result.scalars().all()
        return orders

    async def get_order_items_id_by_id_order_id(
        self,
        id: UUID,
    ):
        stmt = (
            Select(self.model.product_id)
            .where(self.model.order_id == id)
            .options(selectinload(self.model.product))
        )
        result: Result = await self.session.execute(stmt)
        orders = result.scalars().all()
        return orders

    async def update_order_item_status(
        self,
        order_item_id: UUID,
        new_status: OrderItemStatus,
    ) -> OrderItem | None:
        order_item: OrderItem | None = await self.get_by_id(id=order_item_id)

        if not order_item:
            return None
        try:
            order_item.status = new_status
            await self.session.commit()
            await self.session.refresh(order_item)
            return order_item
        except IntegrityError as e:
            await self.session.rollback()
            return None

    async def get_user_ordered_product_ids(
        self,
        user_id: UUID,
    ) -> list[UUID]:
        stmt = Select(self.model.product_id).join(Order).where(Order.user_id == user_id)
        result: Result = await self.session.execute(stmt)
        product_ids = result.scalars().all()
        return product_ids
