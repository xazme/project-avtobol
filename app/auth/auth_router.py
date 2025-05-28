from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, Response
from app.user import UserCreate
from app.token import TokenResponse, create_token_response, TokenMode
from .auth_schema import AuthCredentials
from .auth_dependencies import (
    AuthHandler,
    get_auth_handler,
    get_user_from_refresh_token,
)

if TYPE_CHECKING:
    from app.user import User
    from app.token import Token

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post(
    "/sign-in",
    response_model=TokenResponse,
)
async def auth(
    response: Response,
    credentials: AuthCredentials = Depends(),
    auth_handler: "AuthHandler " = Depends(get_auth_handler),
) -> TokenResponse:
    user: "User" = await auth_handler.sign_in(
        email=credentials.email,
        password=credentials.password,
    )
    token: "Token" = await create_token_response(
        mode=TokenMode.SIGNIN,
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
    user: "User" = await auth_handler.register(user_data=data)
    token: "Token" = await create_token_response(
        mode=TokenMode.REGISTER,
        response=response,
        user=user,
        token_handler=auth_handler.token_handler,
    )
    return TokenResponse.model_validate(token)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    response_model_exclude_none=True,
)
async def get_new_access(
    response: Response,
    user: "User" = Depends(get_user_from_refresh_token),
    auth_handler: "AuthHandler " = Depends(get_auth_handler),
):
    token = await create_token_response(
        mode=TokenMode.REFRESH,
        user=user,
        response=response,
        token_handler=auth_handler.token_handler,
    )
    token.refresh_token = None
    return TokenResponse.model_validate(token)
