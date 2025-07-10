from uuid import UUID
from sqlalchemy import Select, Result
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class ProductMixin:
    async def get_by_product_id(
        self,
        product_id: UUID,
    ):
        stmt = Select(self.model).where(self.model.product_id == product_id)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def update_by_product_id(
        self,
        product_id: UUID,
        data: dict,
    ):
        product = await self.get_by_product_id(product_id=product_id)
        if product is None:
            return None
        try:
            for key, value in data.items():
                setattr(product, key, value)

            await self.session.commit()
            await self.session.refresh(product)
            return product
        except IntegrityError:
            await self.session.rollback()
            return None

    async def update_or_create(self, product_id: UUID, data: dict):
        instance = await self.get_by_product_id(product_id)
        if instance:
            return await self.update_by_product_id(product_id, data)
        else:
            return await self.create(data)
