from sqlalchemy import Select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, DeclarativeBase
from app.shared import BaseCRUD


class ProductRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: DeclarativeBase):
        super().__init__(
            session=session,
            model=model,
        )

    async def get_all(self):
        stmt = Select(self.model).options(
            selectinload(self.model.brand),
            selectinload(self.model.series),
            selectinload(self.model.car_part),
        )
        result: Result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_part_by_id(self, id: int):
        stmt = (
            Select(self.model)
            .where(self.model.id == id)
            .options(
                selectinload(self.model.brand).joinedload(self.model.brand.series),
                selectinload(self.model.car_part),
            )
        )

        result: Result = self.session.execute(statement=stmt)
        return result.scalar_one_or_none()
