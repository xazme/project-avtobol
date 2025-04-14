from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends

from app.user import UserResponce
from app.token import (
    TokenShema,
    get_token_service,
)
from app.shared import Roles
from .auth_dependencies import (
    authentificate_user,
    user_from_refresh_token,
)
from .auth_helper import requied_roles

if TYPE_CHECKING:
    from app.token import TokenService, TokenShema
    from app.user import User, UserResponce


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/sign-in")
async def auth(
    user: "User" = Depends(authentificate_user),
    token_service: "TokenService" = Depends(get_token_service),
) -> TokenShema:

    user_data: dict = {
        "id": user.id,
        "username": user.obj_name,
        "email": user.email,
    }

    access_token = token_service.generate_access_token(data=user_data)
    refresh_token = token_service.generate_refresh_token(data=user_data)

    return TokenShema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


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
    response_model=TokenShema,
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

    return TokenShema(access_token=access_token)
