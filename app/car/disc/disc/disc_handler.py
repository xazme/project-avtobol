from app.shared import BaseHandler
from .disc_repository import DiscRepository


class DiscHandler(BaseHandler):

    def __init__(self, repository: DiscRepository):
        super().__init__(repository)
        self.repository: DiscRepository = repository
