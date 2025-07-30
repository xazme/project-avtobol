from app.shared import BaseHandler
from .cart_item_repository import CartItemRepository


class CartItemHandler(BaseHandler):

    def __init__(self, repository: CartItemRepository):
        super().__init__(repository)
        self.repository: CartItemRepository = repository
