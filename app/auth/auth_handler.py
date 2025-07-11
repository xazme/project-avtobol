from uuid import UUID
from typing import TYPE_CHECKING, Optional
from fastapi import Response
from fastapi.security.http import HTTPAuthorizationCredentials
from app.user import UserCreate

from app.cart.cart import CartCreate
from app.cart.cart import CartHandler
from app.token import TokenType
from app.shared import HashHelper, ExceptionRaiser
from app.core import settings

if TYPE_CHECKING:
    from app.user import User, UserHandler
    from app.token import TokenHandler, Token


class AuthHandler:
    def __init__(
        self,
        user_handler: "UserHandler",
        token_handler: "TokenHandler",
        cart_handler: "CartHandler",
    ):
        self.user_handler = user_handler
        self.token_handler = token_handler
        self.cart_handler = cart_handler

    async def sign_in(
        self,
        phone_number: str,
        password: str,
    ) -> Optional["User"]:
        user = await self.user_handler.get_user_by_phone_number(phone_number)
        if not user or not HashHelper.check_password(password, user.password):
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Неверный логин или пароль.",
            )
        return user

    async def sign_out(
        self,
        user_id: UUID,
        response: Response,
    ):
        result = await self.token_handler.delete_refresh_token_by_user_id(user_id)
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Не удалось выйти из системы.",
            )
        response.delete_cookie(settings.auth.refresh_token_key)

    async def register(
        self,
        user_data: "UserCreate",
    ) -> Optional["User"]:
        user = await self.user_handler.create_user(data=user_data)
        user_id = user.id
        await self.cart_handler.create_obj(CartCreate(user_id=user_id))
        return user_id

    async def user_from_access_token(
        self,
        auth_credentials: HTTPAuthorizationCredentials,
    ) -> Optional["User"]:
        token = self.__ensure_valid_token(auth_credentials=auth_credentials)
        payload: dict = self.token_handler.manager.decode(
            token=token,
            type=TokenType.ACCESS,
        )
        user_id: Optional[UUID] = payload.get("id")

        if not user_id:
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="В токене отсутствует id пользователя.",
            )

        user: "User" | None = await self.user_handler.get_user_by_id(user_id=user_id)
        if not user:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Пользоватеь не найден.",
            )

        return user

    async def user_from_refresh_token(
        self,
        refresh_token: str,
    ) -> Optional["User"]:
        if refresh_token is None:
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="Невалидный refresh токен.",
            )

        refresh_token: "Token" | None = await self.token_handler.get_refresh_token(
            token=refresh_token,
        )
        if not refresh_token:
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="Невалидный refresh токен.",
            )

        payload: dict = self.token_handler.manager.decode(
            token=refresh_token.refresh_token,
            type=TokenType.REFRESH,
        )
        user_id: Optional[UUID] = payload.get("id")

        if not user_id:
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="В токене отсутствует id пользователя.",
            )

        user: "User" | None = await self.user_handler.get_user_by_id(user_id=user_id)
        if not user:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Пользователь не найден.",
            )

        return user

    def __ensure_valid_token(
        self,
        auth_credentials: HTTPAuthorizationCredentials | None,
    ) -> str:
        if not auth_credentials or not isinstance(
            auth_credentials, HTTPAuthorizationCredentials
        ):
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="Токен потерян либо невалиден.",
            )
        return auth_credentials.credentials
