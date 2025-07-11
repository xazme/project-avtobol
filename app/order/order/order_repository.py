from uuid import UUID
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseCRUD
from .order_model import Order


class OrderRepository(BaseCRUD):

    def __init__(self, session: AsyncSession, model: Order):
        super().__init__(session=session, model=model)
        self.session: AsyncSession = session
        self.model: Order = model
