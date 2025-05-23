from pydantic import BaseModel
from app.shared import BaseHandler, ExceptionRaiser, HashHelper, Roles
from .user_repository import UserRepository


class UserHandler(BaseHandler):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)
        self.repository: UserRepository = repository

    async def create(self, data: BaseModel):
        new_data = data.model_copy(
            update={
                "password": HashHelper.hash_password(password=data.password),
                "role": Roles.CLIENT,
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

    async def get_by_name(self, name: str):
        user = await self.repository.get_by_name(name=name)
        if not user:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Failed to get obj {name}. Location - {self.__class__.__name__}",
            )
        return user

    async def update(self, id: int, data: BaseModel):
        new_data = data.model_copy(
            update={"password": HashHelper.hash_password(password=data.password)}
        )
        data = new_data.model_dump(exclude_unset=True)
        updated_user = await self.repository.update(
            id=id,
            data=data,
        )
        if not updated_user:
            ExceptionRaiser.raise_exception(
                status_code=422,
                detail=f"Failed to update a obj {id}. Location - {self.__class__.__name__}",
            )
        return updated_user
