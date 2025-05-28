from typing import TYPE_CHECKING
from fastapi import Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from app.user import UserCreate
from app.token import TokenType, TokenHandler, get_access_token, get_refresh_token
from app.shared import HashHelper, ExceptionRaiser

if TYPE_CHECKING:
    from app.user import User, UserHandler
    from app.token import TokenHandler, Token


class AuthHandler:

    def __init__(
        self,
        user_handler: "UserHandler",
        token_handler: "TokenHandler",
    ):
        self.user_handler = user_handler
        self.token_handler = token_handler

    async def sign_in(
        self,
        email: str,
        password: str,
    ) -> "User":
        user: "User" = await self.user_handler.get_user_by_email(email=email)
        result = HashHelper.check_password(
            password=password,
            hashed_password=user.password,
        )
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=401, detail="Invalid credentials"
            )
        return user

    async def register(
        self,
        user_data: UserCreate,
    ) -> "User":
        user: "User" = await self.user_handler.create_user(data=user_data)
        return user

    async def user_from_access_token(
        self,
        token: HTTPAuthorizationCredentials = Depends(get_access_token),
    ) -> "User":
        if type(token) != HTTPAuthorizationCredentials:
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="Not Auth",
            )
        token: "Token" = await self.token_handler.get_access_token(
            token=token.credentials,
        )
        payload = self.token_handler.manager.decode(
            token=token.access_token,
            type=TokenType.ACCESS,
        )
        user_id = payload.get("id")
        user: "User" = await self.user_handler.get_user_by_id(user_id=user_id)
        return user

    async def user_from_refresh_token(
        self,
        token: HTTPAuthorizationCredentials = Depends(get_refresh_token),
    ) -> "User":
        if type(token) != HTTPAuthorizationCredentials:
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="Not Auth",
            )
        token: "Token" = await self.token_handler.get_refresh_token(
            token=token.credentials,
        )
        payload = self.token_handler.manager.decode(
            token=token.refresh_token,
            type=TokenType.REFRESH,
        )
        user_id = payload.get("id")
        user: "User" = await self.user_handler.get_user_by_id(user_id=user_id)
        return user
