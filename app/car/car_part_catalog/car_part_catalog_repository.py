from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD


class CarPartCatalogRepository(BaseCRUD):
    def __init__(
        self,
        session: AsyncSession,
        model: DeclarativeBase,
    ):
        super().__init__(
            session=session,
            model=model,
        )
