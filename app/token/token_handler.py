from pydantic import BaseModel
from app.shared import BaseHandler, ExceptionRaiser
from .token_repository import TokenRepository
from .token_manager import TokenManager


class TokenHandler(BaseHandler):

    def __init__(
        self,
        repository: TokenRepository,
        manager: TokenManager,
    ):
        super().__init__(repository)
        self.repository = repository
        self.manager = manager

    async def create(self, data: BaseModel):
        data = data.model_dump(exclude_unset=True)
        token = await self.repository.create(data=data)
        if not token:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Error while token create",
            )
        return token

    async def get_access_token(self, token: str):
        token = await self.repository.get_access_token(token=token)
        if not token:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Access token not found in database",
            )
        return token

    async def get_refresh_token(self, token: str):
        token = await self.repository.get_refresh_token(token=token)
        if not token:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Refresh token not found in database",
            )
        return token
