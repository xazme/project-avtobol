from sqlalchemy.ext.asyncio import AsyncSession
from .car_part_model import CarPart
from app.shared import CRUDGenerator


class CarPart(CRUDGenerator[CarPart]):

    def __init__(self, session: AsyncSession, model: type[CarPart]):
        super().__init__(session, model)
