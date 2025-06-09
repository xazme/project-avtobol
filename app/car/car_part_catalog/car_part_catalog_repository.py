from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .car_part_catalog_model import CarPart


class CarPartRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: CarPart):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: CarPart = model
