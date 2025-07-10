from app.shared import BaseHandler
from .tire_brand_repository import TireBrandRepository


class TireBrandHandler(BaseHandler):

    def __init__(self, repository: TireBrandRepository):
        super().__init__(repository)
        self.repository: TireBrandRepository = repository
