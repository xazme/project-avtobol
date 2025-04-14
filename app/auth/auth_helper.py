from typing import TYPE_CHECKING
from fastapi import Depends
from app.shared import ExceptionRaiser
from .auth_dependencies import user_from_access_token
from app.shared import Roles

if TYPE_CHECKING:
    from app.user import User


def requied_roles(allowed_roles: list[Roles]) -> "User":
    def get_user(user: "User" = Depends(user_from_access_token)):
        if user.role not in allowed_roles:
            ExceptionRaiser.raise_exception(status_code=404)
        return user

    return get_user
