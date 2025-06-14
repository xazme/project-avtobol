from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .tires_model import Tires


class TiresRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: Tires):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: Tires = model
