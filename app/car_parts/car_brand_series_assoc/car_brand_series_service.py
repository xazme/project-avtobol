from sqlalchemy import Select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from .car_brand_series_model import CarBrandPartSeriesAssoc
from app.shared import CRUDGenerator


class CarBrandSeriesService(CRUDGenerator):

    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=CarBrandPartSeriesAssoc,
        )

    async def get_all(self):
        stmt = Select(self.model).options(
            selectinload(
                self.model.brand,
            ),
            selectinload(
                self.model.part,
            ),
            selectinload(
                self.model.series,
            ),
        )
        result: Result = await self.session.execute(statement=stmt)
        return list(result.scalars())
