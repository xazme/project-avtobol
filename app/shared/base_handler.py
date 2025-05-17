from pydantic import BaseModel
from app.storage import StorageService
from .exceptions import ExceptionRaiser
from .base_crud import BaseCRUD


class BaseHandler:

    def __init__(
        self,
        repository: BaseCRUD,
    ):
        self.repository = repository

    async def create(self, data: BaseModel):
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

    async def get(self, id: int):
        obj = await self.repository.get(id=id)
        if not obj:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Obj {id} not found. Location - {self.__class__.__name__}",
            )
        return obj

    async def get_all(self):
        all_obj = await self.repository.get_all()
        return all_obj

    async def get_by_name(self, name: str):
        obj = self.repository.get_by_name(name=name)
        if not obj:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Obj {id} not found. Location - {self.__class__.__name__}",
            )
        return obj

    async def update(self, id: int, data: BaseModel):
        data = data.model_dump(exclude_unset=True)
        updated_obj = await self.repository.update(
            id=id,
            data=data,
        )
        if not updated_obj:
            ExceptionRaiser.raise_exception(
                status_code=422,
                detail=f"Failed to update a obj {id}. Location - {self.__class__.__name__}",
            )
        return updated_obj

    async def delete(self, id: int):
        result = await self.repository.delete(id=id)
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail=f"Failed to delete a obj {id}. Location - {self.__class__.__name__}",
            )
        return result


# get → fetch_by_id
# create → insert_record
# update → modify_record
# delete → remove_record
# get_by_name → fetch_by_name
# get_all → fetch_all
