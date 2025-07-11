from app.shared import BaseHandler
from .order_repository import OrderRepository


class OrderHandler(BaseHandler):

    def __init__(self, repository: OrderRepository):
        super().__init__(repository)
        self.repository: OrderRepository = repository
