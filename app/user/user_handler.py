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
    ) -> User:
        new_data = data.model_copy(
            update={
                "password": HashHelper.hash_password(password=data.password),
                "role": UserRoles.CLIENT,
                "status": UserStatuses.ACTIVE,
            }
        )
        data = new_data.model_dump(exclude_unset=True)
        user = await self.repository.create(
            data=data,
        )
        if not user:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail=f"Failed to create obj. Location - {self.__class__.__name__}",
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
                detail=f"Failed to delete obj. Location - {self.__class__.__name__}",
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
        updated_user = await self.repository.update_by_id(
            id=user_id,
            data=data,
        )
        if not updated_user:
            ExceptionRaiser.raise_exception(
                status_code=422,
                detail=f"Failed to update a obj {user_id}. Location - {self.__class__.__name__}",
            )
        return updated_user

    async def get_all_users(self) -> list[User]:
        return await self.repository.get_all()

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> User:
        user = await self.repository.get_user_by_id(id=user_id)
        if not user:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"User not found {user_id}. Location - {self.__class__.__name__}",
            )
        return user

    async def get_user_by_name(
        self,
        name: str,
    ) -> User:
        user = await self.repository.get_user_by_name(name=name)
        if not user:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Failed to get obj {name}. Location - {self.__class__.__name__}",
            )
        return user

    async def get_user_by_email(
        self,
        email: EmailStr,
    ) -> User:
        user = await self.repository.get_user_by_email(email=email)
        if not user:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"User not found {email}. Location - {self.__class__.__name__}",
            )
        return user
