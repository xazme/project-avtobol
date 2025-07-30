from typing import Optional
from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .token_repository import TokenRepository
from .token_manager import TokenManager
from .token_schema import TokenCreate, TokenUpdate
from .token_model import Token


class TokenHandler(BaseHandler):

    def __init__(
        self,
        repository: TokenRepository,
        manager: TokenManager,
    ):
        super().__init__(repository)
        self.repository: TokenRepository = repository
        self.manager: TokenManager = manager

    async def create_token(
        self,
        data: TokenCreate,
    ) -> Optional[Token]:
        data = data.model_dump(exclude_unset=True)
        token = await self.repository.create(data=data)
        if not token:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Мы не можем создать токен.",
            )
        return token

    async def delete_refresh_token_by_user_id(
        self,
        user_id: UUID,
    ) -> bool:
        result = await self.repository.delete_refresh_token_by_user_id(user_id=user_id)
        return result

    async def get_all_tokens(
        self,
    ) -> list[Token]:
        return await self.get_all_obj()

    async def get_refresh_token(
        self,
        token: str,
    ) -> Optional[Token]:
        token_obj = await self.repository.get_refresh_token_by_token(token=token)
        if not token_obj:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Рефреш токен на найден.",
            )
        return token_obj
