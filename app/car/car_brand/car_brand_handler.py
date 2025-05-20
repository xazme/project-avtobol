from fastapi import UploadFile
from pydantic import BaseModel
from app.shared import ExceptionRaiser
from app.shared import BaseHandler
from app.storage import StorageService


class CarSeriesHandler(BaseHandler):

    def __init__(self, repository, storage: StorageService):
        self.storage = storage
        super().__init__(repository)

    async def create(self, file: bytes | UploadFile, data: BaseModel):
        filename = await self.storage.create_file(file)
        car_brand_data = data.model_copy()
        car_brand_data.picture = filename
        car_brand_data_upd = car_brand_data.model_dump()

        brand = await self.repository.create(data=car_brand_data_upd)
        if not brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"We cant create a object. Location - {self.__class__.__name__}",
            )
        return brand

    async def delete(self, id: int):
        brand = await self.repository.get(id=id)
        if not brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Obj {id} not found. Location - {self.__class__.__name__}",
            )

        await self.storage.delete_file(brand.picture)
        await self.repository.delete(id=id)

    async def update(self, id: int, data: BaseModel, file: bytes | UploadFile = None):
        brand = await self.repository.get(id=id)
        if not brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Obj {id} not found. Location - {self.__class__.__name__}",
            )

        if file:
            if brand.picture:
                await self.storage.delete_file(brand.picture)
            filename = await self.storage.create_file(file)
            data.picture = filename

        updated_data = data.model_dump(exclude_unset=True)

        updated_brand = await self.repository.update(id=id, data=updated_data)
        if not updated_brand:
            ExceptionRaiser.raise_exception(
                status_code=422,
                detail=f"Failed to update obj {id}. Location - {self.__class__.__name__}",
            )

        return updated_brand
