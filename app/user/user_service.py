from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import CRUDGenerator
from .user_model import User


class UserService(CRUDGenerator[User]):

    def __init__(self, session: AsyncSession, model: type[User]):
        super().__init__(session=session, model=model)
