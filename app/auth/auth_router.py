from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, Response, status
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

router = APIRouter(
    tags=["Authentication"],
    prefix="/auth",
)


@router.post(
    "/sign-in",
    summary="User sign-in",
    description="Authenticate user with email and password",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def sign_in(
    response: Response,
    credentials: AuthCredentials,
    auth_handler: AuthHandler = Depends(get_auth_handler),
) -> TokenResponse:
    user = await auth_handler.sign_in(
        email=credentials.email,
        password=credentials.password,
    )
    token = await create_token_response(
        mode=TokenMode.SIGNIN,
        user=user,
        token_handler=auth_handler.token_handler,
        response=response,
    )
    return TokenResponse.model_validate(token)


@router.post(
    "/register",
    summary="User registration",
    description="Create a new user account",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    response: Response,
    user_data: UserCreate,
    auth_handler: AuthHandler = Depends(get_auth_handler),
) -> TokenResponse:
    user = await auth_handler.register(user_data=user_data)
    token = await create_token_response(
        mode=TokenMode.REGISTER,
        user=user,
        token_handler=auth_handler.token_handler,
        response=response,
    )
    return TokenResponse.model_validate(token)


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Generate new access token using refresh token",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def refresh_access_token(
    response: Response,
    user: "User" = Depends(get_user_from_refresh_token),
    auth_handler: AuthHandler = Depends(get_auth_handler),
) -> TokenResponse:
    token = await create_token_response(
        mode=TokenMode.REFRESH,
        user=user,
        token_handler=auth_handler.token_handler,
        response=response,
    )
    token.refresh_token = None
    return TokenResponse.model_validate(token)
