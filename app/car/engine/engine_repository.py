from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .engine_model import Engine
from ..shared import ProductMixin


class EngineRepository(BaseCRUD, ProductMixin):

    def __init__(self, session: AsyncSession, model: Engine):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: Engine = model
