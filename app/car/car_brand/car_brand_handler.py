from typing import Optional
from uuid import UUID
from fastapi import UploadFile
from app.shared import ExceptionRaiser, BaseHandler
from app.storage import StorageHandler
from .car_brand_schema import (
    CarBrandCreate,
    CarBrandUpdate,
)
from .car_brand_repository import CarBrandRepository
from .car_brand_model import CarBrand


# TODO TO ORCHESTRATOR
class CarBrandHandler(BaseHandler):

    def __init__(self, repository: CarBrandRepository, storage: StorageHandler):
        super().__init__(repository)
        self.repository: CarBrandRepository = repository
        self.storage: StorageHandler = storage

    async def create_car_brand(
        self,
        car_brand_data: CarBrandCreate,
        file: UploadFile,
    ) -> CarBrand:
        car_brand = await self.repository.get_by_name(name=car_brand_data.name)
        if car_brand:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail=f"Марка {car_brand_data.name} уже существует.",
            )

        self.__validate_files([file])
        try:
            file_bytes = await file.read()
        except Exception:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Не удалось прочитать файл лого.",
            )

        filename = await self.storage.create_file(file=file_bytes)
        data = car_brand_data.model_dump(exclude_unset=True)
        data.update({"picture": filename})

        new_brand = await self.repository.create(data=data)
        if not new_brand:
            await self.storage.delete_file(filename=filename)
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Ошибка во время создания марки.",
            )

        return new_brand

    async def update_car_brand(
        self,
        car_brand_id: UUID,
        car_brand_data: CarBrandUpdate,
        file: UploadFile | None,
    ) -> CarBrand:
        car_brand: CarBrand = await self.repository.get_by_id(id=car_brand_id)
        if not car_brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Марка {car_brand_id} не существует.",
            )

        old_picture = car_brand.picture
        new_filename = None
        data = car_brand_data.model_dump(exclude_unset=True)

        if file:
            self.__validate_files([file])
            try:
                file_bytes = await file.read()
            except Exception:
                ExceptionRaiser.raise_exception(
                    status_code=400,
                    detail="Не удалось прочитать файл.",
                )

            new_filename = await self.storage.create_file(file=file_bytes)
            data.update({"picture": new_filename})

        updated_brand = await self.repository.update_by_id(id=car_brand_id, data=data)
        if not updated_brand:
            if new_filename:
                await self.storage.delete_file(filename=new_filename)
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Ошибка во время обновления марки.",
            )

        if new_filename and old_picture:
            await self.storage.delete_file(filename=old_picture)

        return updated_brand

    async def delete_car_brand(self, car_brand_id: UUID) -> bool:
        brand: CarBrand = await self.repository.get_by_id(id=car_brand_id)
        if not brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Марка {car_brand_id} не найдена.",
            )
        result = await self.repository.delete_by_id(id=car_brand_id)
        if result and brand.picture:
            await self.storage.delete_file(filename=brand.picture)

        return result

    async def get_all_brands(
        self,
        query: str,
        page: int | None,
        page_size: int | None,
    ) -> list[CarBrand]:
        return await self.get_all_obj_pagination(
            query=query,
            page=page,
            page_size=page_size,
        )

    async def get_car_brand_by_id(
        self,
        car_brand_id: UUID,
    ) -> CarBrand:
        brand: CarBrand | None = await self.get_obj_by_id(id=car_brand_id)
        if not brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Марка не найдена.",
            )
        return brand

    def __validate_files(self, files: list[UploadFile]) -> None:
        allowed_formats = {
            "image/jpeg",
            "image/png",
            "image/webp",
            "application/octet-stream",
        }

        for file in files:
            if file.content_type not in allowed_formats:
                ExceptionRaiser.raise_exception(
                    status_code=400,
                    detail=(
                        f"Неверный формат файла: {file.content_type}. "
                        f"Допустимые форматы: {', '.join(allowed_formats)}."
                    ),
                )
