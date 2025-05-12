from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD


class CarSeriesRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: DeclarativeBase):
        super().__init__(session, model)
