from uuid import UUID
from sqlalchemy import Select, Update, Result, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import OperationalError
from app.shared import BaseCRUD
from app.car.car_brand import CarBrand
from .product_model import Product
from .product_schema import ProductFiltersExtended, ProductFilters
from ..tire import Tire
from ..disc import Disc
from ..engine import Engine
from ..tire.tire import TireFilters
from ..disc.disc import DiscFilters
from ..engine import EngineFilters


class ProductRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: Product):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: Product = model

    async def get_all_products_by_scroll(
        self,
        cursor: int | None,
        take: int | None,
        main_filters: ProductFilters | ProductFiltersExtended | None,
        tire_filters: TireFilters | None,
        disc_filters: DiscFilters | None,
        engine_filters: EngineFilters | None,
        is_private: bool = False,
    ) -> tuple[list[Product], int]:
        product_filters: list = await self.prepare_filters(
            filters_main=main_filters,
            filters_tire=tire_filters,
            filters_disc=disc_filters,
            filters_engine=engine_filters,
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
                selectinload(self.model.tire),
                selectinload(self.model.disc),
                selectinload(self.model.engine),
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
        main_filters: ProductFilters | ProductFiltersExtended | None,
        tire_filters: TireFilters | None,
        disc_filters: DiscFilters | None,
        engine_filters: EngineFilters | None,
        is_private: bool = False,
    ) -> tuple[list[Product], int]:
        product_filters: list = await self.prepare_filters(
            filters_main=main_filters,
            filters_tire=tire_filters,
            filters_disc=disc_filters,
            filters_engine=engine_filters,
            is_private=is_private,
        )

        stmt: Select = (
            Select(self.model)
            .options(
                selectinload(self.model.car_brand),
                selectinload(self.model.car_series),
                selectinload(self.model.car_part),
                selectinload(self.model.tire),
                selectinload(self.model.disc),
                selectinload(self.model.engine),
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
        filters_main: ProductFilters | ProductFiltersExtended | None,
        filters_tire: TireFilters | None,
        filters_disc: DiscFilters | None,
        filters_engine: EngineFilters | None,
        is_private: bool,
    ) -> list:
        filters_list: list = []

        if filters_main.article:
            filters_list.append(self.model.article.ilike(f"{filters_main.article}%"))
        if filters_main.car_brand_id:
            filters_list.append(self.model.car_brand_id == filters_main.car_brand_id)
        if filters_main.car_series_id:
            filters_list.append(self.model.car_series_id == filters_main.car_series_id)
        if filters_main.car_part_id:
            filters_list.append(self.model.car_part_id == filters_main.car_part_id)
        if filters_main.price_from:
            filters_list.append(self.model.price >= filters_main.price_from)
        if filters_main.price_to:
            filters_list.append(self.model.price <= filters_main.price_to)
        if filters_main.year_from:
            filters_list.append(self.model.year >= filters_main.year_from)
        if filters_main.year_to:
            filters_list.append(self.model.year <= filters_main.year_to)
        if filters_main.type_of_body:
            filters_list.append(self.model.type_of_body == filters_main.type_of_body)
        if filters_main.condition:
            filters_list.append(self.model.condition == filters_main.condition)
        if filters_main.availability:
            filters_list.append(self.model.availability == filters_main.availability)

        if filters_tire.diametr:
            filters_list.append(Tire.diametr == filters_tire.diametr)
        if filters_tire.width:
            filters_list.append(Tire.width == filters_tire.width)
        if filters_tire.height:
            filters_list.append(Tire.height == filters_tire.height)
        if filters_tire.index:
            filters_list.append(Tire.index == filters_tire.index)
        if filters_tire.car_type:
            filters_list.append(Tire.car_type == filters_tire.car_type)
        if filters_tire.brand_id:
            filters_list.append(Tire.tire_brand_id == filters_tire.brand_id)
        if filters_tire.model:
            filters_list.append(Tire.model.ilike(f"{filters_tire.model}%"))
        if filters_tire.season:
            filters_list.append(Tire.season == filters_tire.season)
        if filters_tire.residue_from:
            filters_list.append(Tire.residue >= filters_tire.residue_from)
        if filters_tire.residue_to:
            filters_list.append(Tire.residue <= filters_tire.residue_to)

        if filters_disc.diametr:
            filters_list.append(Disc.diametr == filters_disc.diametr)
        if filters_disc.width:
            filters_list.append(Disc.width == filters_disc.width)
        if filters_disc.ejection:
            filters_list.append(Disc.ejection == filters_disc.ejection)
        if filters_disc.dia:
            filters_list.append(Disc.dia == filters_disc.dia)
        if filters_disc.holes:
            filters_list.append(Disc.holes == filters_disc.holes)
        if filters_disc.pcd:
            filters_list.append(Disc.pcd == filters_disc.pcd)
        if filters_disc.brand_id:
            filters_list.append(Disc.disc_brand_id == filters_disc.brand_id)
        if filters_disc.model:
            filters_list.append(Disc.model.ilike(f"{filters_disc.model}%"))

        if filters_engine.gearbox:
            filters_list.append(Engine.gearbox == filters_engine.gearbox)
        if filters_engine.fuel:
            filters_list.append(Engine.fuel == filters_engine.fuel)
        if filters_engine.volume:
            filters_list.append(Engine.volume == filters_engine.volume)
        if filters_engine.engine_type:
            filters_list.append(Engine.engine_type == filters_engine.engine_type)

        if is_private:
            if filters_main.created_from:
                filters_list.append(Product.created_at >= filters_main.created_from)
            if filters_main.created_to:
                filters_list.append(Product.created_at <= filters_main.created_to)
            if filters_main.post_by:
                filters_list.append(Product.post_by == filters_main.post_by)
            if filters_main.is_printed is not None:
                filters_list.append(Product.is_printed == filters_main.is_printed)
            if filters_main.is_available is not None:
                filters_list.append(Product.is_available == filters_main.is_available)
        else:
            filters_list.append(Product.is_available.is_(True))

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
                selectinload(self.model.tire),
                selectinload(self.model.disc),
                selectinload(self.model.engine),
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

    async def get_products_by_articles(
        self,
        list_of_articles: list[str],
    ) -> list[Product] | None:
        stmt = Select(self.model.id).where(self.model.article.in_(list_of_articles))
        try:
            result: Result = await self.session.execute(statement=stmt)
            await self.session.commit()
            return result.scalars().all()

        except OperationalError:
            await self.session.rollback()
            return None

    async def bulk_change_availibility(
        self,
        products_id: list[UUID],
        new_availables_status: bool,
    ) -> list[Product] | None:
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
