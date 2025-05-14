from typing import TYPE_CHECKING
from fastapi import Depends
from app.token import get_token_handler
from app.user import get_user_handler
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
