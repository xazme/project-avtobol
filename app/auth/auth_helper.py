from typing import TYPE_CHECKING
from fastapi import Depends, Response
from app.shared import ExceptionRaiser, Roles
from app.token import TokenResponse, TokenCreate, Tokens
from .auth_dependencies import user_from_access_token

if TYPE_CHECKING:
    from app.user import User
    from app.token import TokenService


def requied_roles(allowed_roles: list[Roles]) -> "User":
    def get_user(user: "User" = Depends(user_from_access_token)):
        if user.role not in allowed_roles:
            ExceptionRaiser.raise_exception(status_code=404)
        return user

    return get_user


async def create_token_response(
    mode: Tokens,
    response: Response,
    user: "User",
    token_service: "TokenService",
):

    user_data = {
        "id": user.id,
        "username": user.name,
    }

    access_token = token_service.generate_access_token(data=user_data)
    refresh_token = token_service.generate_refresh_token(data=user_data)

    if mode == Tokens.REFRESH:
        token_data = TokenCreate(
            user_id=user.id,
            access_token=access_token,
        )

        token = await token_service.update_access_token(
            user_id=user.id,
            new_data=token_data.model_dump(exclude_unset=True),
        )

        if not token:
            ExceptionRaiser.raise_exception(
                status_code=500,
                detail="token create error",
            )
        return token

    if mode == Tokens.SIGNIN:
        token_data = TokenCreate(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
        )

        response.set_cookie(
            key=refresh_token,
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )

        deleted_token = await token_service.delete_token(user_id=user.id)
        print(deleted_token)
        token = await token_service.create(token_data.model_dump())
        if not token:
            ExceptionRaiser.raise_exception(
                status_code=500,
                detail="token create error",
            )
        return token
