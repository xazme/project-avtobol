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
                detail="Can Create a token",
            )
        return token

    async def delete(self, id):
        result = await self.repository.delete(id=id)
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Token not found",
            )
        return result

    async def get_access_token(self, token: str):
        token = await self.repository.get_access_token(token=token)
        if not token:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Access token not found in database",
            )
        return token

    async def update_access_token(self, id: int, token: BaseModel):
        token = await self.repository.update_access_token(
            user_id=id,
            data=token.model_dump(exclude_unset=True),
        )
        if not token:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Error while we try to update token",
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
