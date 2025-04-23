from sqlalchemy import Select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from .car_part_model import CarPart
from app.shared import CRUDGenerator


class CarPartService(CRUDGenerator):

    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=CarPart,
        )

    async def get_all(self):
        stmt = Select(self.model).options(
            selectinload(
                self.model.brand_id,
                self.model.part_id,
                self.model.series_id,
            )
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()
