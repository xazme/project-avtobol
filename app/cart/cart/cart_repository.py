from uuid import UUID
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Delete, Select, Result, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .cart_model import Cart


class CartRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: Cart):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: Cart = model

    async def get_user_cart_by_user_id(
        self,
        user_id: UUID,
    ) -> UUID | None:
        stmt = Select(self.model).where(self.model.user_id == user_id)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_user_cart_id_by_user_id(
        self,
        user_id: UUID,
    ) -> Cart | None:
        stmt = Select(self.model.id).where(self.model.user_id == user_id)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()
