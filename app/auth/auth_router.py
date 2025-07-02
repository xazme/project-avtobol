from typing import TYPE_CHECKING
from fastapi import APIRouter, Body, Depends, Response, status
from app.user import UserCreate
from app.token import TokenResponse, create_token_response, TokenMode
from app.core import settings
from app.user.user_enums import UserRoles
from .auth_schema import AuthCredentials
from .auth_dependencies import (
    AuthHandler,
    requied_roles,
    get_auth_handler,
    get_user_from_refresh_token,
)

if TYPE_CHECKING:
    from app.user import User

router = APIRouter(
    prefix=settings.api.auth_prefix,
    tags=["Authentication"],
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
    credentials: AuthCredentials = Body(...),
    auth_handler: AuthHandler = Depends(get_auth_handler),
) -> TokenResponse:
    user = await auth_handler.sign_in(
        phone_number=credentials.phone_number,
        password=credentials.password,
    )
    token = await create_token_response(
        mode=TokenMode.SIGNIN,
        user=user,
        token_handler=auth_handler.token_handler,
        response=response,
    )
    return token


@router.post(
    "/register",
    summary="User registration",
    description="Create a new user account",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    response: Response,
    user_data: UserCreate = Body(...),
    auth_handler: AuthHandler = Depends(get_auth_handler),
) -> TokenResponse:
    user = await auth_handler.register(user_data=user_data)

    token = await create_token_response(
        mode=TokenMode.REGISTER,
        user=user,
        token_handler=auth_handler.token_handler,
        response=response,
    )
    return token


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Generate new access token using refresh token",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
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
    return token


@router.delete(
    "/sign-out",
    summary="Sigh out",
    description="Delete user tokens from database,cookies",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def sign_out(
    response: Response,
    user: "User" = Depends(
        requied_roles(
            allowed_roles=[UserRoles.ADMIN, UserRoles.CLIENT, UserRoles.WORKER]
        )
    ),
    auth_handler: AuthHandler = Depends(get_auth_handler),
):
    await auth_handler.sign_out(user_id=user.id, response=response)
