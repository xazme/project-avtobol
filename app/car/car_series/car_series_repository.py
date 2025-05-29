from uuid import UUID
from sqlalchemy import Select, exists, Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .car_series_model import CarSeries


class CarSeriesRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: CarSeries,
    ):
        super().__init__(session=session, model=model)
        self.model = model
        self.session = session

    async def check_relation(
        self,
        brand_id: UUID,
        series_id: UUID,
    ) -> bool:
        stmt = Select(
            exists().where(
                self.model.id == series_id,
                self.model.brand_id == brand_id,
            )
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar()
