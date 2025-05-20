from app.shared import BaseCRUD
from sqlalchemy import Select, Result, Delete, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession


class CartRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: DeclarativeBase,
    ):
        super().__init__(session, model)

    async def get_positions(self, user_id):
        stmt = Select(self.model).where(self.model.user_id == user_id)
        result: Result = await self.session.execute(statement=stmt)
        positions = result.scalars().all()
        return positions

    async def get_by_position_id(self, position_id):
        stmt = Select(self.model).where(self.model.product_id == position_id)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def delete_position(self, position_id):
        position = await self.get_by_position_id(position_id=position_id)
        if not position:
            return position
        await self.session.delete(position)
        await self.session.commit()
        return True

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
