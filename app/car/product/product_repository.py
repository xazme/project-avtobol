from uuid import UUID
from sqlalchemy import Select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.shared import BaseCRUD
from app.car.car_brand import CarBrand
from .product_model import Product


class ProductRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: Product,
    ):
        super().__init__(session=session, model=model)
        self.session = session
        self.model = model

    async def get_all_products(
        self,
        page: int,
        page_size: int,
    ) -> list[Product]:
        stmt = (
            Select(self.model)
            .options(
                selectinload(self.model.car_brand),
                selectinload(self.model.car_series),
                selectinload(self.model.car_part),
            )
            .order_by(self.model.id)
            .limit(limit=page_size)
            .offset((page - 1) * page_size)
            .where(self.model.is_alailible == True)
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_product_by_id(
        self,
        id: UUID,
    ) -> Product | None:
        stmt = (
            Select(self.model)
            .where(self.model.id == id)
            .options(
                selectinload(self.model.car_brand).joinedload(CarBrand.car_series),
                selectinload(self.model.car_part),
            )
        )

        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def change_availibility(
        self,
        product_id: UUID,
        new_available_status: bool,
    ) -> Product | None:
        product = await self.get_product_by_id(id=product_id)
        try:
            product.is_alailible = new_available_status
            await self.session.commit()
            await self.session.refresh(product)
            return product
        except:
            await self.session.rollback()
            return None

    async def check_availability(
        self,
        product_id: UUID,
    ):
        product = await super().get_by_id(id=product_id)
        # TODO ИСПРАВИТЬ ОШИБКУ
        if product.is_alailible:
            return True
        else:
            return False
