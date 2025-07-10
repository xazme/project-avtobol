from app.shared import BaseHandler
from .cart_repository import CartRepository


class CartHandler(BaseHandler):
    def __init__(self, repository: CartRepository):
        super().__init__(repository)
        self.repository: CartRepository = repository
