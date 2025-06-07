from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.auth import requied_roles
from app.core.config import settings
from app.user.user_schema import UserResponse, UserUpdate
from .user_dependencies import get_user_handler
from .user_model import User
from .user_enums import UserRoles

if TYPE_CHECKING:
    from .user_handler import UserHandler


router = APIRouter(prefix=settings.api.user_prefix, tags=["Users"])


@router.get(
    "/{user_id}",
    summary="Get user by ID",
    description="Retrieve a user by their unique identifier",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    dependencies=[Depends(requied_roles([UserRoles.WORKER]))],
)
async def get_user(
    user_id: UUID,
    user_handler: "UserHandler" = Depends(get_user_handler),
) -> UserResponse:
    user = await user_handler.get_user_by_id(user_id=user_id)
    return UserResponse.model_validate(user)


@router.delete(
    "/{user_id}",
    summary="Delete user by ID",
    description="Delete a user by their unique identifier (Worker access required)",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    dependencies=[Depends(requied_roles([UserRoles.WORKER]))],
)
async def delete_user_by_id(
    user_id: UUID,
    user_handler: "UserHandler" = Depends(get_user_handler),
) -> dict[str, str]:
    await user_handler.delete_user(user_id=user_id)


@router.get(
    "/",
    summary="Get all users",
    description="Retrieve a list of all users in the system",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponse],
    dependencies=[Depends(requied_roles([UserRoles.WORKER]))],
)
async def get_all_users(
    user_handler: "UserHandler" = Depends(get_user_handler),
) -> list[UserResponse]:
    users = await user_handler.get_all_users()
    return [UserResponse.model_validate(user) for user in users]


@router.put(
    "/me/update",
    summary="Update current user",
    description="Update information for the currently authenticated user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def update_current_user(
    user_data: UserUpdate,
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    user_handler: "UserHandler" = Depends(get_user_handler),
) -> UserResponse:
    updated_user = await user_handler.update_user(
        user_id=user.id,
        data=user_data,
    )
    return UserResponse.model_validate(updated_user)


@router.delete(
    "/me/delete",
    summary="Delete current user",
    description="Delete the currently authenticated user account",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_current_user(
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    user_handler: "UserHandler" = Depends(get_user_handler),
) -> dict[str, str]:
    await user_handler.delete_user(user_id=user.id)


@router.patch(
    "/{user_id}/role",
    summary="Change user role",
    description="Change a user's role (Admin or Owner access required)",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    dependencies=[Depends(requied_roles([UserRoles.ADMIN, UserRoles.OWNER]))],
)
async def change_user_role(
    role: UserRoles,
    user_id: UUID,
    user_handler: "UserHandler" = Depends(get_user_handler),
) -> UserResponse:
    updated_user = await user_handler.change_user_role(user_id=user_id, new_role=role)
    return UserResponse.model_validate(updated_user)


@router.get(
    "/me/info",
    summary="Get current user info",
    description="Retrieve information about the currently authenticated user",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_current_user_info(
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
) -> UserResponse:
    return UserResponse.model_validate(user)
