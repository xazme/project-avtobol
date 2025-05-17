from app.shared import BaseHandler


class CartHandler(BaseHandler):
    def __init__(self, repository):
        super().__init__(repository)
