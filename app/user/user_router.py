from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, status
from app.core.config import settings
from app.user.user_schema import UserResponce, UserCreate, UserUpdate
from .user_dependencies import get_user_handler

if TYPE_CHECKING:
    from .user_handler import UserHandler


router = APIRouter(prefix=settings.api.user_prefix, tags=["Users"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserResponce,
)
async def get_user(
    user_id: int,
    user_handler: "UserHandler" = Depends(get_user_handler),
):
    user = await user_handler.get(obj_id=user_id)
    return UserResponce.model_validate(user)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list,
)
async def get_all(
    user_handler: "UserHandler" = Depends(get_user_handler),
):
    users = await user_handler.get_all()
    return [UserResponce.model_validate(user) for user in users]


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserResponce,
)
async def create_user(
    user_data: UserCreate,
    user_service: "UserHandler" = Depends(get_user_handler),
):
    user = await user_service.create(data=user_data)
    return UserResponce.model_validate(user)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserResponce,
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_handler: "UserHandler" = Depends(get_user_handler),
):
    updated_user = await user_handler.update(
        id=user_id,
        data=user_data,
    )

    return UserResponce.model_validate(updated_user)


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def delete_user(
    user_id: int,
    user_handler: "UserHandler" = Depends(get_user_handler),
):
    deleted_user = await user_handler.delete(id=user_id)
    return {"message": "success"}
