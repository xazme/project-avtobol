from uuid import UUID
from sqlalchemy import Select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .tire_model import Tire
from ...shared import ProductMixin


class TireRepository(BaseCRUD, ProductMixin):

    def __init__(self, session: AsyncSession, model: Tire):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: Tire = model
