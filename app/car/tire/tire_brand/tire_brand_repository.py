from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .tire_brand_model import TireBrand


class TireBrandRepository(BaseCRUD):

    def __init__(
        self,
        session: AsyncSession,
        model: TireBrand,
    ):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: TireBrand = model
