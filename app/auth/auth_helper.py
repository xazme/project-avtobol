from typing import TYPE_CHECKING
from fastapi import Depends, Response
from app.shared import ExceptionRaiser, Roles
from app.token import TokenResponse, TokenCreate, Tokens

if TYPE_CHECKING:
    from app.user import User
    from app.token import TokenHandler


# def requied_roles(allowed_roles: list[Roles]) -> "User":
#     def get_user(user: "User" = Depends(user_from_access_token)):
#         if user.role not in allowed_roles:
#             ExceptionRaiser.raise_exception(status_code=404)
#         return user

#     return get_user


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

        token = await token_handler.repository.update_access_token(
            user_id=user.id,
            new_data=token_data.model_dump(exclude_unset=True),
        )

    elif mode == Tokens.SIGNIN:

        response.set_cookie(
            key=refresh_token,
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        await token_handler.repository.delete_token(user_id=user.id)
        token = await token_handler.create(token_data)

    elif mode == Tokens.REGISTER:
        response.set_cookie(
            key=refresh_token,
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        token = await token_handler.repository.create(token_data.model_dump())
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
