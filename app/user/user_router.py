from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.auth import requied_roles
from app.core.config import settings
from app.user.user_schema import UserResponce, UserUpdate
from .user_dependencies import get_user_handler
from .user_model import User
from .user_enums import UserRoles

if TYPE_CHECKING:
    from .user_handler import UserHandler


router = APIRouter(prefix=settings.api.user_prefix, tags=["Users"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserResponce,
    dependencies=[Depends(requied_roles([UserRoles.WORKER]))],
)
async def get_user(
    user_id: UUID,
    user_handler: "UserHandler" = Depends(get_user_handler),
):
    user = await user_handler.get_user_by_id(user_id=user_id)
    return UserResponce.model_validate(user)


@router.delete(
    "/WORK",
    status_code=status.HTTP_200_OK,
    response_model=None,
    dependencies=[Depends(requied_roles([UserRoles.WORKER]))],
)
async def delete_user(
    user_id: UUID,
    user_handler: "UserHandler" = Depends(get_user_handler),
):
    deleted_user = await user_handler.delete_user(user_id=user_id)
    return {"message": "success"}


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponce],
    dependencies=[Depends(requied_roles([UserRoles.WORKER]))],
)
async def get_all(
    user_handler: "UserHandler" = Depends(get_user_handler),
):
    users = await user_handler.get_all_users()
    return [UserResponce.model_validate(user) for user in users]


@router.put(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponce,
)
async def update_user(
    user_data: UserUpdate,
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    user_handler: "UserHandler" = Depends(get_user_handler),
):
    updated_user = await user_handler.update_user(
        user_id=user.id,
        data=user_data,
    )

    return UserResponce.model_validate(updated_user)


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def delete_user(
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    user_handler: "UserHandler" = Depends(get_user_handler),
):
    deleted_user = await user_handler.delete_user(user_id=user.id)
    return {"message": "success"}


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserResponce,
)
async def info(
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
):
    return UserResponce.model_validate(user)
