from typing import TYPE_CHECKING
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from app.user import get_user_handler
from app.token import (
    TokenHandler,
    get_token_handler,
    get_access_token,
    get_refresh_token,
)
from .auth_handler import AuthHandler

if TYPE_CHECKING:
    from app.token import TokenHandler
    from app.user import UserHandler


def get_auth_handler(
    user_handler: "UserHandler" = Depends(get_user_handler),
    token_handler: "TokenHandler" = Depends(get_token_handler),
):
    return AuthHandler(
        user_handler=user_handler,
        token_handler=token_handler,
    )


async def get_user_from_access_token(
    token: HTTPAuthorizationCredentials = Depends(get_access_token),
    auth_handler: "AuthHandler" = Depends(get_auth_handler),
):
    return await auth_handler.user_from_access_token(token)


async def get_user_from_refresh_token(
    token: HTTPAuthorizationCredentials = Depends(get_refresh_token),
    auth_handler: "AuthHandler" = Depends(get_auth_handler),
):
    return await auth_handler.user_from_refresh_token(token)
