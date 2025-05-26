from uuid import UUID
from fastapi import UploadFile
from app.shared import ExceptionRaiser
from app.shared import BaseHandler
from app.storage import StorageService
from .car_brand_schema import CarBrandCreate, CarBrandUpdate
from .car_brand_repository import CarBrandRepository
from .car_brand_model import CarBrand


class CarBrandHandler(BaseHandler):

    def __init__(
        self,
        repository: CarBrandRepository,
        storage: StorageService,
    ):
        super().__init__(repository)
        self.storage = storage
        self.repository = repository

    async def create_brand(
        self,
        file: UploadFile,
        data: CarBrandCreate,
    ):
        file = await file.read()
        filename = await self.storage.create_file(file)
        car_brand_data = data.model_dump(exclude_unset=True)
        car_brand_data.update({"picture": filename})

        brand: CarBrand = await self.repository.create(data=car_brand_data)
        if not brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"We cant create a object. Location - {self.__class__.__name__}",
            )
        return brand

    async def delete_brand(
        self,
        id: UUID,
    ):
        brand: "CarBrand" = await self.repository.get_by_id(id=id)
        if not brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Obj {id} not found. Location - {self.__class__.__name__}",
            )

        await self.storage.delete_file(brand.picture)
        await self.repository.delete_by_id(id=id)

    async def update_brand(
        self,
        id: UUID,
        data: CarBrandUpdate,
        file: UploadFile | None = None,
    ):
        file = await file.read()
        brand: "CarBrand" = await self.repository.get_by_id(id=id)
        if not brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Obj {id} not found. Location - {self.__class__.__name__}",
            )

        if file:
            if brand.picture:
                await self.storage.delete_file(brand.picture)
            filename = await self.storage.create_file(file=file)
            data.picture = filename

        updated_data = data.model_dump(exclude_unset=True)

        updated_brand = await self.repository.update_by_id(id=id, data=updated_data)
        if not updated_brand:
            await self.storage.delete_file(filename=filename)
            ExceptionRaiser.raise_exception(
                status_code=422,
                detail=f"Failed to update obj {id}. Location - {self.__class__.__name__}",
            )

        return updated_brand

    async def get_all_brands(self):
        return await super().get_all_obj()

    async def get_brand_by_id(
        self,
        id: UUID,
    ):
        return await super().get_obj_by_id(id)
