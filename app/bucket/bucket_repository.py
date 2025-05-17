from app.shared import BaseCRUD
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession


class CartRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: DeclarativeBase):
        super().__init__(session, model)
