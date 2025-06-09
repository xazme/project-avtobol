from typing import Optional
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
    ) -> Optional[DeclarativeBase]:
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
    ) -> Optional[DeclarativeBase]:
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
    ) -> Optional[DeclarativeBase]:
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
    ) -> Optional[DeclarativeBase]:
        obj = await self.repository.get_by_id(id=id)
        if not obj:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Obj {id} not found. Location - {self.__class__.__name__}",
            )
        return obj

    async def get_all_obj(
        self,
    ) -> list[DeclarativeBase]:
        all_obj = await self.repository.get_all()
        return all_obj

    async def get_all_obj_pagination(
        self,
        query: str,
        page: int,
        page_size: int,
    ) -> list[DeclarativeBase]:
        return await self.repository.get_all_pagination(
            query=query,
            page=page,
            page_size=page_size,
        )

    async def get_all_obj_by_scroll(
        self,
        query: str,
        cursor: int | None,
        take: int | None,
    ) -> tuple[int | None, list]:
        return await self.repository.get_all_by_scrol(
            query=query,
            cursor=cursor,
            take=take,
        )

    async def get_obj_by_name(
        self,
        name: str,
    ) -> Optional[DeclarativeBase]:
        obj = await self.repository.get_by_name(name=name)
        if not obj:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Obj {name} not found. Location - {self.__class__.__name__}",
            )
        return obj
