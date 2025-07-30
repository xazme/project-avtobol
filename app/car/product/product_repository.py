from uuid import UUID
from sqlalchemy import Select, Update, Result, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import OperationalError, IntegrityError
from app.shared import BaseCRUD
from .product_model import Product
from .product_schema import ProductFiltersPublic, ProductFiltersPrivate
from ..engine import Engine
from ..car_brand import CarBrand
from ..car_series import CarSeries
from ..tire import Tire, TireBrand
from ..disc import Disc, DiscBrand
from ..tire.tire import TireFiltersPublic, TireFiltersPrivate
from ..disc.disc import DiscFiltersPublic, DiscFiltersPrivate
from ..engine import EngineFilters


class ProductRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: Product):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: Product = model

    async def create_product(
        self,
        data: dict,
    ) -> Product | None:
        product: Product = self.model(**data)
        try:
            self.session.add(product)
            await self.session.commit()
            await self.session.refresh(product)

            return product
        except IntegrityError as e:
            print(e)
            await self.session.rollback()
            return None

    async def get_all_products_by_cursor(
        self,
        cursor: int | None,
        take: int | None,
        product_filters: ProductFiltersPublic | ProductFiltersPrivate | None,
        tire_filters: TireFiltersPublic | TireFiltersPrivate | None,
        disc_filters: DiscFiltersPublic | DiscFiltersPrivate | None,
        engine_filters: EngineFilters | None,
    ) -> tuple[int, int, list[Product]]:
        prepared_filters: list = self.prepare_filters(
            product_filters=product_filters,
            tire_filters=tire_filters,
            disc_filters=disc_filters,
            engine_filters=engine_filters,
        )

        cursor = cursor if cursor is not None else 0
        stmt_count: Select = Select(func.count(self.model.id)).where(
            *prepared_filters,
        )

        stmt: Select = (
            Select(self.model)
            .options(
                selectinload(self.model.car_brand),
                selectinload(self.model.car_series),
                selectinload(self.model.car_part),
                selectinload(self.model.engine),
                selectinload(self.model.tire).joinedload(Tire.brand),
                selectinload(self.model.disc).joinedload(Disc.brand),
            )
            .order_by(self.model.created_at)
            .offset(cursor)
            .where(and_(*prepared_filters))
        )
        if take is not None:
            stmt = stmt.limit(take)

        result: Result = await self.session.execute(statement=stmt)
        count_result: Result = await self.session.execute(statement=stmt_count)

        total_count = count_result.scalar()

        next_cursor = (
            cursor + take
            if take is not None and (cursor + take) <= total_count
            else None
        )
        return next_cursor, total_count, result.scalars().all()

    async def get_all_products_by_page(
        self,
        page: int,
        page_size: int,
        product_filters: ProductFiltersPublic | ProductFiltersPrivate | None,
        tire_filters: TireFiltersPublic | TireFiltersPrivate | None,
        disc_filters: DiscFiltersPublic | DiscFiltersPrivate | None,
        engine_filters: EngineFilters | None,
    ) -> tuple[list[Product], int]:
        prepared_filters: list = self.prepare_filters(
            product_filters=product_filters,
            tire_filters=tire_filters,
            disc_filters=disc_filters,
            engine_filters=engine_filters,
        )

        stmt_count: Select = (
            Select(func.count()).select_from(self.model).where(and_(*prepared_filters))
        )
        stmt = (
            Select(self.model)
            .options(
                selectinload(self.model.car_brand),
                selectinload(self.model.car_series),
                selectinload(self.model.car_part),
                selectinload(self.model.engine),
                selectinload(self.model.tire).joinedload(Tire.brand),
                selectinload(self.model.disc).joinedload(Disc.brand),
            )
            .order_by(self.model.created_at)
            .limit(limit=page_size)
            .offset((page - 1) * page_size)
            .where(and_(*prepared_filters))
        )

        product_result: Result = await self.session.execute(stmt)
        count_result: Result = await self.session.execute(stmt_count)

        total_count = count_result.scalar()
        return total_count, product_result.scalars().all()

    def prepare_filters(
        self,
        product_filters: ProductFiltersPublic | ProductFiltersPrivate | None,
        tire_filters: TireFiltersPublic | TireFiltersPrivate | None,
        disc_filters: DiscFiltersPublic | DiscFiltersPublic | None,
        engine_filters: EngineFilters | None,
    ) -> list:

        prepared_product_filters: list = self._prepare_product_filters(
            product_filters=product_filters,
        )
        prepared_tire_filters: list = self._prepare_tire_filters(
            tire_filters=tire_filters,
        )
        prepared_disc_filters: list = self._prepare_disc_filters(
            disc_filters=disc_filters,
        )
        prepared_engine_filters: list = self._prepare_engine_filters(
            engine_filters=engine_filters,
        )

        return (
            prepared_product_filters
            + prepared_tire_filters
            + prepared_disc_filters
            + prepared_engine_filters
        )

    async def get_product_by_id(
        self,
        id: UUID,
    ) -> Product | None:
        stmt = (
            Select(self.model)
            .where(self.model.id == id)
            .options(
                selectinload(self.model.car_brand),
                selectinload(self.model.car_series),
                selectinload(self.model.car_part),
                selectinload(self.model.engine),
                selectinload(self.model.tire).joinedload(Tire.brand),
                selectinload(self.model.disc).joinedload(Disc.brand),
            )
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_product_by_article(
        self,
        article: str,
    ) -> Product | None:
        stmt = (
            Select(self.model)
            .where(self.model.article == article)
            .options(
                selectinload(self.model.car_brand).joinedload(CarBrand.car_series),
                selectinload(self.model.car_part),
                selectinload(self.model.engine),
                selectinload(self.model.tire).joinedload(TireBrand),
                selectinload(self.model.disc).joinedload(DiscBrand),
            )
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_products_by_articles(
        self,
        list_of_articles: list[str],
    ) -> list[Product] | None:
        stmt = Select(self.model).where(self.model.article.in_(list_of_articles))
        try:
            result: Result = await self.session.execute(statement=stmt)
            return result.scalars().all()

        except OperationalError:
            await self.session.rollback()
            return None

    async def get_products_by_ids(
        self,
        list_of_product_ids: list[UUID],
    ) -> list[Product] | None:
        stmt = Select(self.model).where(self.model.id.in_(list_of_product_ids))
        try:
            result: Result = await self.session.execute(statement=stmt)
            return result.scalars().all()

        except OperationalError:
            await self.session.rollback()
            return None

    async def bulk_update_availibility(
        self,
        products_id: list[UUID],
        new_availables_status: bool,
    ) -> list[Product] | None:
        stmt = (
            Update(self.model)
            .where(self.model.id.in_(products_id))
            .values(is_available=new_availables_status)
            .returning(self.model)
        )
        try:
            result: Result = await self.session.execute(statement=stmt)
            await self.session.commit()
            return result.scalars().all()
        except OperationalError:
            await self.session.rollback()
            return None

    async def bulk_update_printed_status(
        self,
        products_id: list[UUID],
        status: bool,
    ) -> list[Product] | None:
        stmt = (
            Update(self.model)
            .where(self.model.id.in_(products_id))
            .values(is_printed=status)
            .returning(self.model)
        )
        try:
            result: Result = await self.session.execute(statement=stmt)
            await self.session.commit()
            return result.scalars().all()
        except OperationalError:
            await self.session.rollback()
            return None

    async def update_product_availability(
        self,
        product_id: UUID,
        status: bool,
    ) -> Product | None:
        product: Product | None = await self.get_by_id(id=product_id)
        if not product:
            return None
        try:
            product.is_available = status
            await self.session.commit()
            await self.session.refresh(product)
            return product
        except IntegrityError as e:
            await self.session.rollback()
            return None

    async def check_availability(
        self,
        product_id: UUID,
    ) -> bool:
        product: Product | None = await self.get_by_id(id=product_id)
        return product.is_available if product else False

    async def upload_product_data(
        self,
        product_id: UUID,
    ) -> Product | None:
        stmt = (
            Select(self.model)
            .where(self.model.id == product_id)
            .options(
                selectinload(self.model.engine),
                selectinload(self.model.tire).joinedload(Tire.brand),
                selectinload(self.model.disc).joinedload(Disc.brand),
            )
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    def _prepare_product_filters(
        self,
        product_filters: ProductFiltersPublic | ProductFiltersPrivate | None,
    ) -> list:
        products_filters_list = []
        if product_filters:

            if product_filters.article:
                products_filters_list.append(
                    self.model.article.ilike(f"{product_filters.article}%")
                )
            if product_filters.price_from:
                products_filters_list.append(
                    self.model.price >= product_filters.price_from,
                )
            if product_filters.price_to:
                products_filters_list.append(
                    self.model.price <= product_filters.price_to,
                )
            if product_filters.year_from:
                products_filters_list.append(
                    self.model.year >= product_filters.year_from,
                )
            if product_filters.year_to:
                products_filters_list.append(
                    self.model.year <= product_filters.year_to,
                )
            if product_filters.type_of_body:
                products_filters_list.append(
                    self.model.type_of_body == product_filters.type_of_body,
                )
            if product_filters.condition:
                products_filters_list.append(
                    self.model.condition == product_filters.condition,
                )
            if product_filters.availability:
                products_filters_list.append(
                    self.model.availability == product_filters.availability,
                )

            if isinstance(product_filters, ProductFiltersPublic):
                if product_filters.car_brand_name:
                    products_filters_list.append(
                        CarBrand.name == product_filters.car_brand_name
                    )
                if product_filters.car_series_name:
                    products_filters_list.append(
                        self.model.car_series.name == product_filters.car_series_name
                    )
                if product_filters.car_part_name:
                    products_filters_list.append(
                        CarSeries.name == product_filters.car_part_name
                    )
                else:
                    print("BAAAAAAAAAAAAAAAAAAAASEEEEEEEEEEEE")
                    products_filters_list.append(self.model.is_available == True)

            elif isinstance(product_filters, ProductFiltersPrivate):
                if product_filters.car_brand_id:
                    products_filters_list.append(
                        self.model.car_brand_id == product_filters.car_brand_id,
                    )
                if product_filters.car_series_id:
                    products_filters_list.append(
                        self.model.car_series_id == product_filters.car_series_id,
                    )
                if product_filters.car_part_id:
                    products_filters_list.append(
                        self.model.car_part_id == product_filters.car_part_id,
                    )
                if product_filters.is_printed is not None:
                    products_filters_list.append(
                        self.model.is_printed == product_filters.is_printed,
                    )
                if product_filters.is_available is not None:
                    products_filters_list.append(
                        self.model.is_available == product_filters.is_available,
                    )
                if product_filters.created_from:
                    products_filters_list.append(
                        self.model.created_at >= product_filters.created_from,
                    )
                if product_filters.created_to:
                    products_filters_list.append(
                        self.model.created_at <= product_filters.created_to,
                    )
                if product_filters.post_by:
                    products_filters_list.append(
                        self.model.post_by == product_filters.post_by,
                    )
        return products_filters_list

    def _prepare_tire_filters(
        self,
        tire_filters: TireFiltersPublic | TireFiltersPrivate | None,
    ) -> list:
        tire_filters_list = []
        if tire_filters:
            if tire_filters.diametr:
                tire_filters_list.append(
                    Tire.diametr == tire_filters.diametr,
                )
            if tire_filters.width:
                tire_filters_list.append(
                    Tire.width == tire_filters.width,
                )
            if tire_filters.height:
                tire_filters_list.append(
                    Tire.height == tire_filters.height,
                )
            if tire_filters.index:
                tire_filters_list.append(
                    Tire.index == tire_filters.index,
                )
            if tire_filters.car_type:
                tire_filters_list.append(
                    Tire.car_type == tire_filters.car_type,
                )
            if tire_filters.model:
                tire_filters_list.append(
                    Tire.model == tire_filters.model,
                )
            if tire_filters.season:
                tire_filters_list.append(
                    Tire.season == tire_filters.season,
                )
            if tire_filters.residue_from:
                tire_filters_list.append(
                    Tire.residue >= tire_filters.residue_from,
                )
            if tire_filters.residue_to:
                tire_filters_list.append(
                    Tire.residue <= tire_filters.residue_to,
                )

            if isinstance(tire_filters, TireFiltersPublic):
                if tire_filters.tire_brand_name:
                    tire_filters_list.append(
                        TireBrand.name == tire_filters.tire_brand_name,
                    )

            elif isinstance(tire_filters, TireFiltersPrivate):
                if tire_filters.tire_brand_id:
                    tire_filters_list.append(
                        Tire.tire_brand_id == tire_filters.tire_brand_id,
                    )
        return tire_filters_list

    def _prepare_disc_filters(
        self,
        disc_filters: DiscFiltersPublic | DiscFiltersPublic | None,
    ) -> list:
        disc_filters_list = []
        if disc_filters:
            if disc_filters.diametr:
                disc_filters_list.append(
                    Disc.diametr == disc_filters.diametr,
                )
            if disc_filters.width:
                disc_filters_list.append(
                    Disc.width == disc_filters.width,
                )
            if disc_filters.ejection:
                disc_filters_list.append(
                    Disc.ejection == disc_filters.ejection,
                )
            if disc_filters.dia:
                disc_filters_list.append(
                    Disc.dia == disc_filters.dia,
                )
            if disc_filters.holes:
                disc_filters_list.append(
                    Disc.holes == disc_filters.holes,
                )
            if disc_filters.pcd:
                disc_filters_list.append(
                    Disc.pcd == disc_filters.pcd,
                )
            if disc_filters.model:
                disc_filters_list.append(
                    Disc.model == disc_filters.model,
                )

            if isinstance(disc_filters, DiscFiltersPublic):
                if disc_filters.disc_brand_name:
                    disc_filters_list.append(
                        DiscBrand.name == disc_filters.disc_brand_name,
                    )
            elif isinstance(disc_filters, DiscFiltersPrivate):
                if disc_filters.disc_brand_id:
                    disc_filters_list.append(
                        Disc.disc_brand_id == disc_filters.disc_brand_id,
                    )
        return disc_filters_list

    def _prepare_engine_filters(
        self,
        engine_filters: EngineFilters | None,
    ) -> list:
        engine_filters_list = []
        if engine_filters:
            if engine_filters.gearbox:
                engine_filters_list.append(Engine.gearbox == engine_filters.gearbox)
            if engine_filters.fuel:
                engine_filters_list.append(
                    Engine.fuel == engine_filters.fuel,
                )
            if engine_filters.volume:
                engine_filters_list.append(
                    Engine.volume == engine_filters.volume,
                )
            if engine_filters.engine_type:
                engine_filters_list.append(
                    Engine.engine_type == engine_filters.engine_type,
                )
        return engine_filters_list
