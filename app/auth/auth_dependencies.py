from typing import TYPE_CHECKING
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from app.token.token_dependencies import (
    get_access_token,
    get_refresh_token,
    get_token_handler,
)
from app.shared import ExceptionRaiser
from app.user.user_dependencies import get_user_handler
from app.cart.cart.cart_dependencies import get_cart_handler
from app.auth.auth_handler import AuthHandler

if TYPE_CHECKING:
    from app.cart.cart import CartHandler
    from app.user import User, UserHandler
    from app.token import TokenHandler


def get_auth_handler(
    user_handler: "UserHandler" = Depends(get_user_handler),
    token_handler: "TokenHandler" = Depends(get_token_handler),
    cart_handler: "CartHandler" = Depends(get_cart_handler),
) -> AuthHandler:
    return AuthHandler(
        user_handler=user_handler,
        token_handler=token_handler,
        cart_handler=cart_handler,
    )


async def get_user_from_access_token(
    auth_credentials: HTTPAuthorizationCredentials = Depends(get_access_token),
    auth_handler: AuthHandler = Depends(get_auth_handler),
) -> "User":
    return await auth_handler.user_from_access_token(auth_credentials=auth_credentials)


async def get_user_from_refresh_token(
    token: str = Depends(get_refresh_token),
    auth_handler: AuthHandler = Depends(get_auth_handler),
) -> "User":
    return await auth_handler.user_from_refresh_token(refresh_token=token)
