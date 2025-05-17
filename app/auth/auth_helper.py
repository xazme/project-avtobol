from typing import TYPE_CHECKING
from fastapi import Depends, Response
from app.shared import ExceptionRaiser, Roles, Statuses
from app.token import (
    TokenCreate,
    Tokens,
)
from .auth_dependencies import get_user_from_access_token, get_user_from_refresh_token

if TYPE_CHECKING:
    from app.user import User
    from app.token import TokenHandler


def requied_roles(allowed_roles: list[Roles]) -> "User":
    async def get_user(user: "User" = Depends(get_user_from_access_token)):
        if user.status != Statuses.ACTIVE:
            ExceptionRaiser.raise_exception(status_code=303)
        if user.role not in allowed_roles:
            ExceptionRaiser.raise_exception(status_code=303)
        return user

    return get_user


async def create_token_response(
    mode: Tokens,
    user: "User",
    token_handler: "TokenHandler",
    response: Response,
):
    user_data = {
        "id": user.id,
        "username": user.name,
    }

    access_token = token_handler.manager.generate_access_token(data=user_data)
    refresh_token = token_handler.manager.generate_refresh_token(data=user_data)

    token_data = TokenCreate(
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token,
    )

    if mode == Tokens.REFRESH:
        token_data_for_refresh = TokenCreate(
            user_id=user.id,
            access_token=access_token,
        )

        token = await token_handler.update_access_token(
            id=user.id,
            token=token_data_for_refresh,
        )

    elif mode == Tokens.SIGNIN:

        response.set_cookie(
            key=refresh_token,
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        await token_handler.delete(id=user.id)
        token = await token_handler.create(token_data)

    elif mode == Tokens.REGISTER:
        response.set_cookie(
            key=refresh_token,
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        token = await token_handler.create(data=token_data)
    else:
        ExceptionRaiser.raise_exception(
            status_code=400,
            detail="Invalid token mode",
        )

    if not token:
        ExceptionRaiser.raise_exception(
            status_code=500,
            detail="token create error",
        )

    return token
