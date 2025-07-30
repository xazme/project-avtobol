from app.shared import BaseHandler
from .tire_repository import TireRepository


class TireHandler(BaseHandler):

    def __init__(self, repository: TireRepository):
        super().__init__(repository)
        self.repository: TireRepository = repository
