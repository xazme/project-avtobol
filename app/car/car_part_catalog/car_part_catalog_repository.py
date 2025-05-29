from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .car_part_catalog_model import CarPartCatalog


class CarPartCatalogRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: CarPartCatalog,
    ):
        super().__init__(session=session, model=model)
        self.model = model
        self.session = session
