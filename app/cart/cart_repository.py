from app.shared import BaseCRUD
from sqlalchemy import Select, Result, Delete, func, Insert
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession


class CartRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: DeclarativeBase,
    ):
        super().__init__(session, model)

    async def get_all_positions(self, user_id):
        stmt = Select(self.model).where(self.model.user_id == user_id)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_position(self, position_id: int, user_id: int):
        stmt = (
            Select(self.model)
            .where(self.model.product_id == position_id)
            .where(self.model.user_id == user_id)
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def delete_position(self, position_id: int, user_id: int):
        position = await self.get_position(position_id=position_id, user_id=user_id)
        if not position:
            return None
        await self.session.delete(position)
        await self.session.commit()
        return True

    async def add_position(
        self,
        data: dict,
    ):
        position = await self.get_position(
            position_id=data.get("product_id"),
            user_id=data.get("user_id"),
        )

        if position:
            return None

        position = self.model(**data)
        self.session.add(position)
        await self.session.commit()
        await self.session.refresh(position)
        return position

    async def delete_all_positions(self, user_id: int):
        count: Result = await self.session.execute(
            Select(func.count())
            .select_from(self.model)
            .where(self.model.user_id == user_id)
        )
        if count.scalar() <= 0:
            return None
        stmt = Delete(self.model).where(self.user_id == user_id)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()
