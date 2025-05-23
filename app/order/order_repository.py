from app.shared import BaseCRUD, OrderStatuses
from sqlalchemy import Select, Delete, Result
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


class OrderRepository(BaseCRUD):
    def __init__(
        self,
        session: AsyncSession,
        model: DeclarativeBase,
    ):
        super().__init__(session, model)

    async def get_user_orders(
        self,
        user_id: int,
    ):
        stmt = Select(self.model).where(self.model.user_id == user_id)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_user_order(
        self,
        user_id: int,
        product_id: int,
    ):
        stmt = (
            Select(self.model)
            .where(self.model.user_id == user_id)
            .where(self.model.product_id == product_id)
        )

        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def create_order(self, data: dict):
        existing_order = await self.get_user_order(
            user_id=data.get("user_id"),
            product_id=data.get("product.id"),
        )

        if existing_order:
            return None

        order = self.model(**data)
        self.session.add(order)

        await self.session.commit()
        return order

    async def create_orders(self, positions: list):
        try:
            self.session.add_all(positions)
            await self.session.commit()
            return positions
        except IntegrityError:
            await self.session.rollback()
            return None

    async def delete_order(self, user_id: int, product_id: int):
        user_order = await self.get_user_order(user_id=user_id, product_id=product_id)
        if not user_order:
            return None
        self.session.delete(user_order)
        await self.session.commit()
        return True

    async def get_all_orders(self):
        stmt = Select(self.model)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_all_active_orders(self):
        stmt = Select(self.model).where(self.model.status == OrderStatuses.OPEN)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_all_closed_orders(self):
        stmt = Select(self.model).where(self.model.status == OrderStatuses.CLOSED)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_all_denied_orders(self):
        stmt = Select(self.model).where(self.model.status == OrderStatuses.DENIED)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_active_user_orders(self, user_id: int):
        stmt = (
            Select(self.model)
            .where(self.model.user_id == user_id)
            .where(self.model.status == OrderStatuses.OPEN)
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_closed_user_orders(self, user_id: int):
        stmt = (
            Select(self.model)
            .where(self.model.user_id == user_id)
            .where(self.model.status == OrderStatuses.CLOSED)
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_denied_user_orders(self, user_id: int):
        stmt = (
            Select(self.model)
            .where(self.model.user_id == user_id)
            .where(self.model.status == OrderStatuses.DENIED)
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()
