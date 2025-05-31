from uuid import UUID
from fastapi import UploadFile
from app.shared import ExceptionRaiser, BaseHandler
from app.storage import StorageService
from .car_brand_schema import CarBrandCreate, CarBrandUpdate
from .car_brand_repository import CarBrandRepository
from .car_brand_model import CarBrand
from typing import Optional


class CarBrandHandler(BaseHandler):

    def __init__(self, repository: CarBrandRepository, storage: StorageService):
        super().__init__(repository)
        self.storage: StorageService = storage
        self.repository: CarBrandRepository = repository

    async def create_car_brand(
        self,
        file: UploadFile,
        data: CarBrandCreate,
    ) -> Optional[CarBrand]:
        allowed_formats = [
            "image/jpeg",
            "application/octet-stream",
            "image/png",
            "image/webp",
        ]
        if file.content_type not in allowed_formats:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail=f"Wrong file extension. Allowed formats - {allowed_formats}. Get {file.content_type}",
            )

        file_bytes: bytes = await file.read()
        filename: str = await self.storage.create_file(file_bytes)
        car_brand_data: dict = data.model_dump(exclude_unset=True)
        car_brand_data.update({"picture": filename})

        brand: CarBrand | None = await self.repository.create(data=car_brand_data)
        if not brand:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Failed to create car brand.",
            )
        return brand

    async def delete_car_brand(
        self,
        car_brand_id: UUID,
    ) -> bool:
        brand: CarBrand | None = await self.repository.get_by_id(id=car_brand_id)
        if not brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Car brand {car_brand_id} not found.",
            )

        await self.storage.delete_file(brand.picture)
        result: bool = await self.repository.delete_by_id(id=car_brand_id)
        return result

    async def update_car_brand(
        self,
        car_brand_id: UUID,
        data: CarBrandUpdate,
        file: UploadFile | None = None,
    ) -> CarBrand:
        brand: CarBrand | None = await self.repository.get_by_id(id=car_brand_id)
        if not brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Car brand {car_brand_id} not found.",
            )

        if file:
            allowed_formats = [
                "image/jpeg",
                "application/octet-stream",
                "image/png",
                "image/webp",
            ]
            if file.content_type not in allowed_formats:
                ExceptionRaiser.raise_exception(
                    status_code=400,
                    detail=f"Wrong file extension. Allowed formats - {allowed_formats}. Get {file.content_type}",
                )
            if brand.picture:
                await self.storage.delete_file(brand.picture)
            filename: str = await self.storage.create_file(await file.read())

        updated_data: dict = data.model_dump(exclude_unset=True)

        if filename:
            updated_data.update({"picture": filename})

        updated_brand: CarBrand | None = await self.repository.update_by_id(
            id=car_brand_id, data=updated_data
        )
        if not updated_brand:
            if file:
                await self.storage.delete_file(filename)
            ExceptionRaiser.raise_exception(
                status_code=422,
                detail=f"Failed to update car brand {car_brand_id}.",
            )

        return updated_brand

    async def get_all_brands(
        self,
    ) -> list[CarBrand]:
        return await self.get_all_obj()

    async def get_car_brand_by_id(
        self,
        car_brand_id: UUID,
    ) -> CarBrand:
        brand: CarBrand | None = await self.get_obj_by_id(id=car_brand_id)
        if not brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Car brand not found.",
            )
        return brand
