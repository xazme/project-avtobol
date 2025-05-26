from uuid import UUID
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase
from .exceptions import ExceptionRaiser
from .base_crud import BaseCRUD


class BaseHandler:

    def __init__(
        self,
        repository: BaseCRUD,
    ):
        self.repository = repository

    async def create_obj(
        self,
        data: BaseModel,
    ) -> DeclarativeBase | None:
        data = data.model_dump(exclude_unset=True)
        obj = await self.repository.create(
            data=data,
        )
        if not obj:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail=f"Failed to create obj {data}. Location - {self.__class__.__name__}",
            )
        return obj

    async def update_obj(
        self,
        id: UUID,
        data: BaseModel,
    ) -> DeclarativeBase | None:
        data = data.model_dump(exclude_unset=True)
        updated_obj = await self.repository.update_by_id(
            id=id,
            data=data,
        )
        if not updated_obj:
            ExceptionRaiser.raise_exception(
                status_code=422,
                detail=f"Failed to update a obj {id}. Location - {self.__class__.__name__}",
            )
        return updated_obj

    async def delete_obj(
        self,
        id: UUID,
    ) -> DeclarativeBase | None:
        result = await self.repository.delete_by_id(id=id)
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail=f"Failed to delete a obj {id}. Location - {self.__class__.__name__}",
            )
        return result

    async def get_obj_by_id(
        self,
        id: UUID,
    ) -> DeclarativeBase | None:
        obj = await self.repository.get_by_id(id=id)
        if not obj:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Obj {id} not found. Location - {self.__class__.__name__}",
            )
        return obj

    async def get_all_obj(self) -> DeclarativeBase | None:
        all_obj = await self.repository.get_all()
        return all_obj

    async def get_obj_by_name(
        self,
        name: str,
    ) -> None | DeclarativeBase:
        obj = await self.repository.get_by_name(name=name)
        if not obj:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Obj {name} not found. Location - {self.__class__.__name__}",
            )
        return obj
