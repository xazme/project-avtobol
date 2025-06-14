from uuid import UUID
from sqlalchemy import Select, Update, Result, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import OperationalError
from app.shared import BaseCRUD
from app.car.car_brand import CarBrand
from .product_model import Product
from .product_schema import ProductFilters


class ProductRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: Product):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: Product = model

    async def get_all_products(
        self,
        page: int,
        page_size: int,
        filters: ProductFilters,
    ) -> tuple[list[Product], int]:
        product_filters: list = await self.prepare_filters(filters=filters)
        stmt: Select = (
            Select(self.model)
            .options(
                selectinload(self.model.car_brand),
                selectinload(self.model.car_series),
                selectinload(self.model.car_part),
            )
            .order_by(self.model.created_at)
            .limit(limit=page_size)
            .offset((page - 1) * page_size)
            .where(and_(*product_filters))
        )
        count_stmt: Select = Select(func.count()).where(and_(*product_filters))
        product_result: Result = await self.session.execute(stmt)
        count_result: Result = await self.session.execute(count_stmt)

        return count_result.scalar(), product_result.scalars().all()

    async def prepare_filters(
        self,
        filters: ProductFilters,
    ) -> list:
        filters_list: list = [self.model.is_available == True]
        if filters.car_brand_id:
            filters_list.append(self.model.car_brand_id == filters.car_brand_id)
        if filters.car_series_id:
            filters_list.append(self.model.car_series_id == filters.car_series_id)
        if filters.car_part_id:
            filters_list.append(self.model.car_part_id == filters.car_part_id)
        if filters.price_from:
            filters_list.append(self.model.real_price >= filters.price_from)
        if filters.price_to:
            filters_list.append(self.model.real_price <= filters.price_to)
        if filters.year_from:
            filters_list.append(self.model.year >= filters.year_from)
        if filters.year_to:
            filters_list.append(self.model.year <= filters.year_to)
        if filters.gearbox:
            filters_list.append(self.model.gearbox == filters.gearbox)
        if filters.fuel:
            filters_list.append(self.model.fuel == filters.fuel)
        if filters.condition:
            filters_list.append(self.model.condition == filters.condition)
        if filters.is_available:
            filters_list.append(self.model.is_available == filters.is_available)
        if filters.is_printed:
            filters_list.append(self.model.is_printed == filters.is_printed)
        return filters_list

    async def get_product_by_id(
        self,
        id: UUID,
    ) -> Product | None:
        stmt: Select = (
            Select(self.model)
            .where(self.model.id == id)
            .options(
                selectinload(self.model.car_brand).joinedload(CarBrand.car_series),
                selectinload(self.model.car_part),
            )
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def bulk_change_availibility(
        self,
        products_id: list[UUID],
        new_availables_status: bool,
    ) -> Product | None:
        stmt = (
            Update(self.model)
            .where(self.model.id.in_(products_id))
            .values(is_available=new_availables_status)
        )
        try:
            await self.session.execute(statement=stmt)
            await self.session.commit()
            return True
        except OperationalError:
            await self.session.rollback()
            return False

    async def bulk_change_printed_status(
        self,
        products_id: list[UUID],
        status: bool,
    ) -> bool:
        stmt = (
            Update(self.model)
            .where(self.model.id.in_(products_id))
            .values(is_printed=status)
        )
        try:
            await self.session.execute(statement=stmt)
            await self.session.commit()
            return True
        except OperationalError:
            await self.session.rollback()
            return False

    async def check_availability(
        self,
        product_id: UUID,
    ) -> bool:
        product: Product | None = await self.get_by_id(id=product_id)
        return product.is_available if product else False


{
    "OEM": "string",
    "car_brand_id": "afd8e210-03ab-493f-804b-f8e187330e62",
    "car_series_id": "3d00025f-7943-49bf-b4b3-9f14c7e3bf1e",
    "car_part_id": "0bf56339-5ecb-4ddf-8dac-92b7f15f929b",
    "year": 2000,
    "type_of_body": "sedan",
    "volume": 1.6,
    "gearbox": "manual",
    "fuel": "gasoline",
    "engine_type": "TDI",
    "VIN": "string",
    "pictures": ["photo1.png"],
    "note": "string",
    "description": "string",
    "real_price": 0,
    "fake_price": 0,
    "condition": "used",
    "count": 1,
}
