from uuid import UUID
from pydantic import BaseModel
from app.shared import BaseHandler, ExceptionRaiser
from .token_repository import TokenRepository
from .token_manager import TokenManager
from .token_schema import TokenCreate, TokenUpdate


class TokenHandler(BaseHandler):

    def __init__(
        self,
        repository: TokenRepository,
        manager: TokenManager,
    ):
        super().__init__(repository)
        self.repository = repository
        self.manager = manager

    async def create_token(
        self,
        data: TokenCreate,
    ):
        data = data.model_dump(exclude_unset=True)
        token = await self.repository.create(data=data)
        if not token:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Can Create a token",
            )
        return token

    async def delete_tokens_by_user_id(
        self,
        user_id: UUID,
    ):
        result = await self.repository.delete_tokens_by_user_id(user_id=user_id)
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Token not found",
            )
        return result

    async def update_access_token(
        self,
        id: UUID,
        data: TokenUpdate,
    ):
        token = await self.repository.update_access_token(
            user_id=id,
            data=data.model_dump(exclude_unset=True),
        )
        if not token:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Error while we try to update token",
            )
        return token

    async def get_all_tokens(self):
        return await self.get_all_obj()

    async def get_access_token(
        self,
        token: str,
    ):
        token = await self.repository.get_access_token_by_token(token=token)
        if not token:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Access token not found in database",
            )
        return token

    async def get_refresh_token(
        self,
        token: str,
    ):
        token = await self.repository.get_refresh_token_by_token(token=token)
        if not token:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Refresh token not found in database",
            )
        return token
