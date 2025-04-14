from typing import Annotated, TYPE_CHECKING
from fastapi import APIRouter, Depends, Path
from app.core.config import settings
from app.user.user_schema import UserResponce, UserCreate, UserUpdate
from app.shared import ExceptionRaiser, HashHelper
from .user_dependencies import get_user_service

if TYPE_CHECKING:
    from app.shared import CRUDGenerator


router = APIRouter(prefix=settings.api.user_prefix, tags=["Users"])


@router.get(
    "/",
    response_model=list[UserResponce],
)
async def get_all(user_service: "CRUDGenerator" = Depends(get_user_service)):
    users = await user_service.get_all()
    return [UserResponce.model_validate(user) for user in users]


@router.get("/{user_id}")
async def get_user(
    user_id: Annotated[int, Path()],
    user_service: "CRUDGenerator" = Depends(get_user_service),
):
    user = await user_service.get(obj_id=user_id)
    if not user:
        ExceptionRaiser.raise_exception(status_code=404)
    return UserResponce.model_validate(user)


@router.post("/{user_id}")
async def create_user(
    user_data: UserCreate,
    user_service: "CRUDGenerator" = Depends(get_user_service),
):
    upd_user_data = user_data.copy()
    upd_user_data.password = HashHelper.hash_password(password=user_data.password)
    user = await user_service.create(
        data=upd_user_data.model_dump(
            by_alias=True,
        )
    )
    if not user:
        ExceptionRaiser.raise_exception(status_code=400)
    return UserResponce.model_validate(user)


@router.put("/{user_id}")
async def update_user(
    user_id: Annotated[int, Path()],
    user_data: UserUpdate,
    user_service: "CRUDGenerator" = Depends(get_user_service),
):
    upd_user_data = user_data.copy()
    upd_user_data.password = HashHelper.hash_password(password=user_data.password)

    updated_user = await user_service.update(
        obj_id=user_id,
        new_data=upd_user_data.model_dump(
            by_alias=True,
            exclude_unset=True,
        ),
    )
    if not updated_user:
        ExceptionRaiser.raise_exception(status_code=404)

    return UserResponce.model_validate(updated_user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: Annotated[int, Path()],
    user_service: "CRUDGenerator" = Depends(get_user_service),
):
    deleted_user = await user_service.delete(obj_id=user_id)
    if not deleted_user:
        ExceptionRaiser.raise_exception(status_code=404)
    return {"message": "User deleted successfully"}
