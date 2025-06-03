from uuid import UUID
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Delete, Select, Result, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from app.car.product import Product
from .cart_model import Cart


class CartRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: type[Cart]):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: type[Cart] = model

    async def get_all_user_positions(
        self,
        user_id: UUID,
    ) -> list[Cart]:
        stmt: Select = (
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
        product_id: UUID,
    ) -> Cart | None:
        stmt: Select = Select(self.model).where(
            and_(self.model.user_id == user_id, self.model.product_id == product_id)
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def create_position(
        self,
        user_id: UUID,
        product_id: UUID,
    ) -> Cart | None:
        position: Cart | None = await self.get_user_position(
            user_id=user_id,
            product_id=product_id,
        )
        position_data: dict = {
            "user_id": user_id,
            "product_id": product_id,
        }
        if position:
            return None
        new_position: Cart = self.model(**position_data)
        try:
            self.session.add(new_position)
            await self.session.commit()
            await self.session.refresh(new_position)
            return new_position
        except IntegrityError:
            await self.session.rollback()
            return None

    async def delete_position(
        self,
        user_id: UUID,
        product_id: UUID,
    ) -> bool | None:
        position: Cart | None = await self.get_user_position(
            user_id=user_id,
            product_id=product_id,
        )

        if not position:
            return None

        await self.session.delete(position)
        await self.session.commit()
        return True

    async def delete_all_positions(self, user_id: UUID) -> bool:
        stmt: Delete = Delete(self.model).where(self.model.user_id == user_id)
        result: Result = await self.session.execute(statement=stmt)
        await self.session.commit()
        return True
