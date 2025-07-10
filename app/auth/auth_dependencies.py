from typing import TYPE_CHECKING
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from app.token import get_access_token, get_refresh_token, get_token_handler
from app.user.user_dependencies import get_user_handler
from .auth_handler import AuthHandler

if TYPE_CHECKING:
    from app.token import TokenHandler
    from app.user import UserHandler, User


def get_auth_handler(
    user_handler: "UserHandler" = Depends(get_user_handler),
    token_handler: "TokenHandler" = Depends(get_token_handler),
) -> AuthHandler:
    return AuthHandler(
        user_handler=user_handler,
        token_handler=token_handler,
    )


async def get_user_from_access_token(
    auth_credentials: HTTPAuthorizationCredentials = Depends(get_access_token),
    auth_handler: "AuthHandler" = Depends(get_auth_handler),
) -> "User":
    return await auth_handler.user_from_access_token(auth_credentials=auth_credentials)


async def get_user_from_refresh_token(
    auth_credentials: str = Depends(get_refresh_token),
    auth_handler: "AuthHandler" = Depends(get_auth_handler),
) -> "User":
    return await auth_handler.user_from_refresh_token(refresh_token=auth_credentials)
