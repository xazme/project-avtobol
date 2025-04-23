from sqlalchemy.ext.asyncio import AsyncSession
from .car_part_catalog_model import CarPartCatalog
from app.shared import CRUDGenerator


class CarPartCatalogService(CRUDGenerator):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=CarPartCatalog,
        )
