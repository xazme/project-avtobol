from app.shared import BaseHandler
from .engine_repository import EngineRepository


class EngineHandler(BaseHandler):

    def __init__(self, repository: EngineRepository):
        super().__init__(repository)
        self.repository: EngineRepository = repository
