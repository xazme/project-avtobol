from uuid import UUID
from app.shared import BaseCRUD
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Delete, Select, Result, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.car.product import Product
from .cart_model import Cart


class CartRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: Cart,
    ):
        super().__init__(
            session,
            model,
        )

    async def get_all_user_positions(
        self,
        user_id: UUID,
    ):
        stmt = (
            Select(self.model)
            .where(self.model.user_id == user_id)
            .options(
                joinedload(self.model.product).joinedload(Product.car_brand),
                joinedload(self.model.product).joinedload(Product.car_series),
                joinedload(self.model.product).joinedload(Product.car_part),
            )
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_user_position(
        self,
        user_id: UUID,
        position_id: UUID,
    ):
        stmt = Select(self.model).where(
            and_(self.model.user_id == user_id, self.model.position_id == position_id)
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def create_position(
        self,
        user_id: UUID,
        position_id: UUID,
    ):
        position = await self.get_user_position(
            user_id=user_id,
            position_id=position_id,
        )

        if position:
            return None

        try:
            self.session.add(position)
            await self.session.commit()
            await self.session.refresh(position)
            return position
        except IntegrityError:
            await self.session.rollback()
            return None

    async def delete_position(
        self,
        user_id: UUID,
        position_id: UUID,
    ):
        position = await self.get_user_position(
            user_id=user_id,
            position_id=position_id,
        )

        if not position:
            return None

        await self.session.delete(position)
        await self.session.commit()
        return True

    async def delete_all_positions(
        self,
        user_id: UUID,
    ):
        stmt = Delete(self.model).where(self.model.user_id == user_id)
        result: Result = await self.session.execute(statement=stmt)
        return True
