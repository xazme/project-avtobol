from sqlalchemy.ext.asyncio import AsyncSession
from .car_part_catalog_model import CarPartCatalog
from app.shared import CRUDGenerator


class CarPartCatalogService(CRUDGenerator[CarPartCatalog]):
    def __init__(self, session: AsyncSession, model: type[CarPartCatalog]):
        return CRUDGenerator(session=session, model=model)
