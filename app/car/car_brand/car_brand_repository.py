from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .car_brand_model import CarBrand


class CarBrandRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: CarBrand,
    ):
        super().__init__(session=session, model=model)
        self.model = model
        self.session = session
