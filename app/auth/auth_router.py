from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBasicCredentials
from app.user import UserResponce, UserCreate
from app.token import TokenResponse, Tokens, get_token_handler, create_token_response
from app.shared import Roles
from .auth_dependencies import (
    AuthHandler,
    get_auth_handler,
    requied_roles,
    get_user_from_refresh_token,
)

if TYPE_CHECKING:
    from app.token import TokenHandler
    from app.user import User


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post(
    "/sign-in",
    response_model=TokenResponse,
)
async def auth(
    response: Response,
    credentials: HTTPBasicCredentials = Depends(),
    auth_handler: "AuthHandler " = Depends(get_auth_handler),
) -> TokenResponse:
    user = await auth_handler.sign_in(
        username=credentials.username,
        password=credentials.password,
    )
    token = await create_token_response(
        mode=Tokens.SIGNIN,
        user=user,
        token_handler=auth_handler.token_handler,
        response=response,
    )
    return TokenResponse.model_validate(token)


@router.post(
    "/register",
    response_model=TokenResponse,
)
async def register(
    response: Response,
    data: UserCreate,
    auth_handler: "AuthHandler " = Depends(get_auth_handler),
):
    user = await auth_handler.register(user_data=data)
    token = await create_token_response(
        mode=Tokens.REGISTER,
        response=response,
        user=user,
        token_handler=auth_handler.token_handler,
    )
    return TokenResponse.model_validate(token)


@router.get(
    "/me",
    response_model=UserResponce,
)
async def info(
    user: "User" = Depends(requied_roles([Roles.CLIENT])),
):
    return UserResponce.model_validate(user)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    response_model_exclude_unset=True,
)
async def get_new_access(
    response: Response,
    user: "User" = Depends(get_user_from_refresh_token),
    token_handler: "TokenHandler" = Depends(get_token_handler),
):
    return await create_token_response(
        mode=Tokens.REFRESH,
        user=user,
        response=response,
        token_handler=token_handler,
    )
