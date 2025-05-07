from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import CRUDGenerator
from .car_brand_model import CarBrand


class CarBrandService(CRUDGenerator):

    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model=CarBrand,
        )
