from typing import TYPE_CHECKING, Callable
from fastapi import Depends
from app.shared import ExceptionRaiser
from app.user.user_enums import UserRoles, UserStatuses
from .auth_dependencies import get_user_from_access_token

if TYPE_CHECKING:
    from app.user import User


def required_roles(allowed_roles: list[UserRoles]) -> Callable:
    async def guard(user: "User" = Depends(get_user_from_access_token)):
        if user.status != UserStatuses.ACTIVE:
            ExceptionRaiser.raise_exception(
                status_code=403,
                detail="Аккаунт забанен.",
            )
        if user.role not in allowed_roles:
            ExceptionRaiser.raise_exception(
                status_code=403,
                detail="Недостаточно прав.",
            )
        return user

    return guard
