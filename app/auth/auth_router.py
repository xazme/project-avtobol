from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends
from app.user import UserResponce, UserCreate, get_user_service
from app.token import (
    TokenResponse,
    TokenCreate,
    get_token_service,
)
from app.shared import Roles
from .auth_dependencies import (
    authentificate_user,
    user_from_refresh_token,
)
from .auth_helper import requied_roles

if TYPE_CHECKING:
    from app.token import TokenService
    from app.user import User


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/sign-in")
async def auth(
    user: "User" = Depends(authentificate_user),
    token_service: "TokenService" = Depends(get_token_service),
) -> TokenResponse:

    user_data: dict = {
        "id": user.id,
        "username": user.name,
    }

    access_token = token_service.generate_access_token(data=user_data)
    refresh_token = token_service.generate_refresh_token(data=user_data)

    return TokenResponse(
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/register")
async def register(
    user,
    token_service: "TokenService" = Depends(get_token_service),
):
    data: dict = {
        "id": user.id,
        "username": user.name,
    }

    access_token = token_service.generate_access_token(data=data)
    refresh_token = token_service.generate_refresh_token(data=data)

    token_data = TokenCreate(
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token,
    )
    await token_service.create(token_data.model_dump())

    return TokenResponse.model_validate(token_data)


@router.get(
    "/me",
    response_model=UserResponce,
)
async def info(
    user: "User" = Depends(requied_roles([Roles.WORKER, Roles.SEO, Roles.OWNER])),
):
    return UserResponce.model_validate(user)


@router.get(
    "/refresh",
    response_model=TokenResponse,
    response_model_exclude_unset=True,
)
async def get_new_access(
    user: "User" = Depends(user_from_refresh_token),
    token_service: "TokenService" = Depends(get_token_service),
):

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

    access_token = token_service.generate_access_token(data=user_data)

    return TokenResponse(access_token=access_token)
