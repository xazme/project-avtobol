from typing import TYPE_CHECKING
from fastapi import Depends, Form
from fastapi.security.http import HTTPAuthorizationCredentials
from app.shared import ExceptionRaiser, HashHelper
from app.token import get_access_token, get_refresh_token, get_token_service, Tokens
from app.user import get_user_service, UserCreate

if TYPE_CHECKING:
    from app.user import User, UserService
    from app.shared import UserService
    from app.token import TokenService


async def authentificate_user(
    username: str = Form(strict=True),
    password: str = Form(strict=True),
    user_service: "UserService" = Depends(get_user_service),
) -> "User":

    if not isinstance(username, str) or not isinstance(password, str):
        ExceptionRaiser.raise_exception(
            status_code=401,
            detail="Invalid credentials",
        )

    user: "User" = await user_service.get_by_name(name=username)

    if not user:
        ExceptionRaiser.raise_exception(status_code=404, detail="User Not Found")

    result = HashHelper.check_password(password=password, hashed_password=user.password)

    if not result:
        ExceptionRaiser.raise_exception(status_code=401, detail="Invalid credentials")

    return user


async def register_user(
    user_data: UserCreate,
    user_service: "UserService" = Depends(get_user_service),
):
    upd_user_data = user_data.model_copy()
    upd_user_data.password = HashHelper.hash_password(password=user_data.password)

    data = upd_user_data.model_dump()
    user: "User" = await user_service.create(data=data)
    if not user:
        ExceptionRaiser.raise_exception(
            status_code=404,
            detail="User could not be created",
        )
    return user


async def user_from_refresh_token(
    token: HTTPAuthorizationCredentials = Depends(get_refresh_token),
    user_service: "UserService" = Depends(get_user_service),
    token_service: "TokenService" = Depends(get_token_service),
) -> "User":

    token = token.credentials
    refresh_token = await token_service.get_refresh_token(token=token)
    if not refresh_token:
        ExceptionRaiser.raise_exception(status_code=404, detail="Token Not Found")

    user_data: dict = token_service.decode(token=token, type=Tokens.REFRESH)
    user_id = user_data.get("id")
    user: "User" = await user_service.get(id=user_id)

    if not user:
        ExceptionRaiser.raise_exception(status_code=404, detail="User Not Found")

    return user


async def user_from_access_token(
    token: HTTPAuthorizationCredentials = Depends(get_access_token),
    user_service: "UserService" = Depends(get_user_service),
    token_service: "TokenService" = Depends(get_token_service),
) -> "User":
    user_data: dict = token_service.decode(token=token.credentials, type=Tokens.ACCESS)

    user_id = user_data.get("id")
    user: "User" = await user_service.get(id=user_id)

    if not user:
        ExceptionRaiser.raise_exception(status_code=404, detail="User Not Found")

    return user
