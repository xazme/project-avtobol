from app.shared import BaseHandler
from .disc_brand_repository import DiscBrandRepository


class DiscBrandHandler(BaseHandler):

    def __init__(self, repository: DiscBrandRepository):
        super().__init__(repository)
        self.repository: DiscBrandRepository = repository
