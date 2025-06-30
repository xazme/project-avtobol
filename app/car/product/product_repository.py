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

    async def get_all_products_by_scroll(
        self,
        filters: ProductFilters,
        cursor: int | None,
        take: int | None,
        is_private: bool = False,
    ) -> tuple[list[Product], int]:
        product_filters: list = await self.prepare_filters(
            filters=filters,
            is_private=is_private,
        )
        cursor = cursor if cursor is not None else 0
        stmt_count: Select = Select(func.count(self.model.id))
        stmt_count_using_filters = Select(func.count(self.model.id)).where(
            *product_filters,
        )
        stmt: Select = (
            Select(self.model)
            .options(
                selectinload(self.model.car_brand),
                selectinload(self.model.car_series),
                selectinload(self.model.car_part),
                selectinload(self.model.disc_brand),
                selectinload(self.model.tire_brand),
            )
            .order_by(self.model.created_at)
            .offset(cursor)
            .where(and_(*product_filters))
        )
        if take is not None:
            stmt = stmt.limit(take)

        result: Result = await self.session.execute(statement=stmt)
        result_count: Result = await self.session.execute(statement=stmt_count)
        result_count_with_filters: Result = await self.session.execute(
            statement=stmt_count_using_filters
        )
        count = result_count.scalar()
        count_with_filters = result_count_with_filters.scalar()
        next_cursor = (
            cursor + take if take is not None and (cursor + take) <= count else None
        )
        return next_cursor, count_with_filters, result.scalars().all()

    async def get_all_products(
        self,
        page: int,
        page_size: int,
        filters: ProductFilters,
        is_private: bool = False,
    ) -> tuple[list[Product], int]:
        product_filters: list = await self.prepare_filters(
            filters=filters,
            is_private=is_private,
        )

        stmt: Select = (
            Select(self.model)
            .options(
                selectinload(self.model.car_brand),
                selectinload(self.model.car_series),
                selectinload(self.model.car_part),
                selectinload(self.model.disc_brand),
                selectinload(self.model.tire_brand),
            )
            .order_by(self.model.created_at)
            .limit(limit=page_size)
            .offset((page - 1) * page_size)
            .where(and_(*product_filters))
        )
        count_stmt: Select = (
            Select(func.count()).select_from(self.model).where(and_(*product_filters))
        )
        product_result: Result = await self.session.execute(stmt)
        count_result: Result = await self.session.execute(count_stmt)

        return count_result.scalar(), product_result.scalars().all()

    async def prepare_filters(
        self,
        is_private: bool,
        filters: ProductFilters,
    ) -> list:
        filters_list: list = []

        # Основные
        if filters.article:
            filters_list.append(self.model.article == filters.article)
        if filters.car_brand_id:
            filters_list.append(self.model.car_brand_id == filters.car_brand_id)
        if filters.car_series_id:
            filters_list.append(self.model.car_series_id == filters.car_series_id)
        if filters.car_part_id:
            filters_list.append(self.model.car_part_id == filters.car_part_id)
        if filters.price_from:
            filters_list.append(self.model.price >= filters.price_from)
        if filters.price_to:
            filters_list.append(self.model.price <= filters.price_to)
        if filters.year_from:
            filters_list.append(self.model.year >= filters.year_from)
        if filters.year_to:
            filters_list.append(self.model.year <= filters.year_to)
        if filters.volume:
            filters_list.append(self.model.volume == filters.volume)
        if filters.fuel:
            filters_list.append(self.model.fuel == filters.fuel)
        if filters.gearbox:
            filters_list.append(self.model.gearbox == filters.gearbox)
        if filters.type_of_body:
            filters_list.append(self.model.type_of_body == filters.type_of_body)
        if filters.condition:
            filters_list.append(self.model.condition == filters.condition)
        if filters.availability:
            filters_list.append(self.model.availability == filters.availability)

        # Диски
        if filters.disc_diametr:
            filters_list.append(self.model.disc_diametr == filters.disc_diametr)
        if filters.disc_width:
            filters_list.append(self.model.disc_width == filters.disc_width)
        if filters.disc_ejection:
            filters_list.append(self.model.disc_ejection == filters.disc_ejection)
        if filters.disc_dia:
            filters_list.append(self.model.disc_dia == filters.disc_dia)
        if filters.disc_holes:
            filters_list.append(self.model.disc_holes == filters.disc_holes)
        if filters.disc_pcd:
            filters_list.append(self.model.disc_pcd == filters.disc_pcd)
        if filters.disc_brand_id:
            filters_list.append(self.model.disc_brand_id == filters.disc_brand_id)
        if filters.disc_model:
            filters_list.append(self.model.disc_model.ilike(f"%{filters.disc_model}%"))

        # Шины
        if filters.tires_diametr:
            filters_list.append(self.model.tire_diametr == filters.tires_diametr)
        if filters.tires_width:
            filters_list.append(self.model.tire_width == filters.tires_width)
        if filters.tires_height:
            filters_list.append(self.model.tire_height == filters.tires_height)
        if filters.tires_index:
            filters_list.append(self.model.tire_index == filters.tires_index)
        if filters.tires_car_type:
            filters_list.append(self.model.tire_car_type == filters.tires_car_type)
        if filters.tires_brand_id:
            filters_list.append(self.model.tire_brand_id == filters.tires_brand_id)
        if filters.tires_model:
            filters_list.append(self.model.tire_model.ilike(f"%{filters.tires_model}%"))
        if filters.tires_season:
            filters_list.append(self.model.tire_season == filters.tires_season)
        if filters.tires_residue_from:
            filters_list.append(self.model.tire_residue >= filters.tires_residue_from)
        if filters.tires_residue_to:
            filters_list.append(self.model.tire_residue <= filters.tires_residue_to)

        if is_private:
            if filters.created_from:
                filters_list.append(self.model.created_at >= filters.created_from)
            if filters.created_to:
                filters_list.append(self.model.created_at <= filters.created_to)
            if filters.post_by:
                filters_list.append(self.model.post_by == filters.post_by)
            if filters.is_printed is not None:
                filters_list.append(self.model.is_printed == filters.is_printed)
            if filters.is_available is not None:
                filters_list.append(self.model.is_available == filters.is_available)
        else:
            filters_list.append(self.model.is_available == True)

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

    async def get_product_by_article(
        self,
        article: str,
    ) -> Product | None:
        stmt: Select = (
            Select(self.model)
            .where(self.model.article == article)
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
