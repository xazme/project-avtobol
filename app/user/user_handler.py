from typing import Optional
from uuid import UUID
from pydantic import EmailStr
from app.shared import BaseHandler, ExceptionRaiser, HashHelper
from .user_repository import UserRepository
from .user_schema import UserCreate, UserUpdate
from .user_model import User
from .user_enums import UserRoles, UserStatuses


class UserHandler(BaseHandler):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)
        self.repository: UserRepository = repository

    async def create_user(
        self,
        data: UserCreate,
    ) -> Optional[User]:
        new_data = data.model_copy(
            update={
                "password": HashHelper.hash_password(password=data.password),
                "role": UserRoles.CLIENT,
                "status": UserStatuses.ACTIVE,
            }
        )
        data = new_data.model_dump(exclude_unset=True)

        user = await self.repository.create(data=data)
        if not user:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Неудалось создать пользователя.",
            )

        return user

    async def delete_user(
        self,
        user_id: UUID,
    ) -> bool:
        result = await self.repository.delete_by_id(id=user_id)
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Пользователь {user_id} не найден.",
            )

        return result

    async def update_user(
        self,
        user_id: UUID,
        data: UserUpdate,
    ) -> User:
        new_data = data.model_copy(
            update={"password": HashHelper.hash_password(password=data.password)}
        )
        data = new_data.model_dump(exclude_unset=True)

        updated_user = await self.repository.update_by_id(id=user_id, data=data)
        if not updated_user:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail=f"Неудалось обновить пользователя {user_id}.",
            )

        return updated_user

    async def change_user_role(
        self,
        user_id: UUID,
        new_role: UserRoles,
    ) -> User:
        user = await self.repository.change_user_role(id=user_id, new_role=new_role)
        if not user:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail="Недостаточно прав для смены роли.",
            )

        return user

    async def get_all_users(
        self,
    ) -> list[User]:
        return await self.repository.get_all()

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> User:
        user = await self.repository.get_user_by_id(id=user_id)
        if not user:
            ExceptionRaiser.raise_exception(
                404, f"Пользователь с id {user_id} не найден."
            )

        return user

    async def get_user_by_name(
        self,
        name: str,
    ) -> User:
        user = await self.repository.get_user_by_name(name=name)
        if not user:
            ExceptionRaiser.raise_exception(
                404, f"Пользователь с именем {name} не найден."
            )

        return user

    async def get_user_by_phone_number(
        self,
        phone_number: EmailStr,
    ) -> User:
        user = await self.repository.get_user_by_phone_number(phone_number=phone_number)
        if not user:
            ExceptionRaiser.raise_exception(
                404, f"Пользователь с номером телефона {phone_number} не найден."
            )
        return user
