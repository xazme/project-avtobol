from app.shared import BaseHandler
from .order_item_repository import OrderItemRepository


class OrderItemHandler(BaseHandler):

    def __init__(self, repository: OrderItemRepository):
        super().__init__(repository)
        self.repository: OrderItemRepository = repository
