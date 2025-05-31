from uuid import UUID
from typing import TYPE_CHECKING, Optional
from fastapi import Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from app.user import UserCreate
from app.token import TokenType, TokenHandler, get_access_token, get_refresh_token
from app.shared import HashHelper, ExceptionRaiser

if TYPE_CHECKING:
    from app.user import User, UserHandler
    from app.token import TokenHandler, Token


class AuthHandler:

    def __init__(self, user_handler: "UserHandler", token_handler: "TokenHandler"):
        self.user_handler: UserHandler = user_handler
        self.token_handler: TokenHandler = token_handler

    async def sign_in(
        self,
        email: str,
        password: str,
    ) -> Optional["User"]:
        user: "User" | None = await self.user_handler.get_user_by_email(email=email)
        if not user:
            ExceptionRaiser.raise_exception(
                status_code=401, detail="Invalid credentials"
            )

        result: bool = HashHelper.check_password(
            password=password, hashed_password=user.password
        )
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=401, detail="Invalid credentials"
            )

        return user

    async def register(
        self,
        user_data: UserCreate,
    ) -> Optional["User"]:
        user: "User" = await self.user_handler.create_user(data=user_data)
        return user

    async def user_from_access_token(
        self,
        token: HTTPAuthorizationCredentials = Depends(get_access_token),
    ) -> Optional["User"]:
        if not isinstance(
            token,
            HTTPAuthorizationCredentials,
        ):
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="Not authenticated",
            )

        access_token: "Token" | None = await self.token_handler.get_access_token(
            token=token.credentials
        )
        if not access_token:
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="Invalid access token",
            )

        payload: dict = self.token_handler.manager.decode(
            token=access_token.access_token,
            type=TokenType.ACCESS,
        )
        user_id: Optional[UUID] = payload.get("id")

        if not user_id:
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="User ID missing in token",
            )

        user: "User" | None = await self.user_handler.get_user_by_id(user_id=user_id)
        if not user:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="User not found",
            )

        return user

    async def user_from_refresh_token(
        self,
        token: HTTPAuthorizationCredentials = Depends(get_refresh_token),
    ) -> Optional["User"]:
        if not isinstance(token, HTTPAuthorizationCredentials):
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="Not authenticated",
            )

        refresh_token: "Token" | None = await self.token_handler.get_refresh_token(
            token=token.credentials,
        )
        if not refresh_token:
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="Invalid refresh token",
            )

        payload: dict = self.token_handler.manager.decode(
            token=refresh_token.refresh_token,
            type=TokenType.REFRESH,
        )
        user_id: Optional[UUID] = payload.get("id")

        if not user_id:
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="User ID missing in token",
            )

        user: "User" | None = await self.user_handler.get_user_by_id(user_id=user_id)
        if not user:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="User not found",
            )

        return user
