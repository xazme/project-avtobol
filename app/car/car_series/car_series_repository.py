from uuid import UUID
from sqlalchemy import Select, exists, Result, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from ..product import Product
from .car_series_model import CarSeries


class CarSeriesRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: CarSeries):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: CarSeries = model

    async def check_relation(
        self,
        car_brand_id: UUID,
        car_series_id: UUID,
    ) -> bool:
        stmt: Select = Select(
            exists().where(
                self.model.id == car_series_id,
                self.model.car_brand_id == car_brand_id,
            )
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar()

    async def get_series_by_car_brand_id(
        self,
        car_brand_id: UUID,
    ) -> list[CarSeries]:
        stmt: Select = Select(self.model).where(self.model.car_brand_id == car_brand_id)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_all_series_by_scroll_and_brand_id(
        self,
        query: str,
        cursor: int | None,
        take: int | None,
        car_brand_id: UUID,
    ) -> tuple[int | None, list]:
        cursor = cursor if cursor is not None else 0
        stmt_count: Select = Select(func.count(self.model.id))
        stmt: Select = (
            Select(self.model)
            .offset(cursor)
            .where(
                self.model.car_brand_id == car_brand_id,
                self.model.name.like(f"{query}%"),
            )
        )
        if take is not None:
            stmt = stmt.limit(take)

        result: Result = await self.session.execute(statement=stmt)
        result_count: Result = await self.session.execute(statement=stmt_count)
        count = result_count.scalar()

        next_cursor = (
            cursor + take if take is not None and (cursor + take) <= count else None
        )

        return next_cursor, result.scalars().all()

    async def get_car_series_with_available_parts(
        self,
        car_brand_id: UUID,
    ) -> list["CarSeries"]:
        stmt = Select(self.model).where(
            self.model.car_brand_id == car_brand_id,
            exists().where(
                Product.car_series_id == self.model.id,
                Product.is_available == True,
            ),
        )

        result: Result = await self.session.execute(stmt)
        return result.scalars().all()
