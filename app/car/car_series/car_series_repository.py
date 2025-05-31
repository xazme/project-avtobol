from uuid import UUID
from sqlalchemy import Select, exists, Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
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
