from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .disc_model import DiscBrand


class DiscRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: DiscBrand):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: DiscBrand = model
