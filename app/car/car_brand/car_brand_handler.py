from typing import Optional
from uuid import UUID
import base64
from fastapi import UploadFile
from app.shared import ExceptionRaiser, BaseHandler
from app.storage import StorageService
from app.faststream import broker
from .car_brand_schema import (
    CarBrandCreate,
    CarBrandUpdate,
    CarBrandCreateMessage,
    CarBrandUpdateMessage,
)
from .car_brand_repository import CarBrandRepository
from .car_brand_model import CarBrand


class CarBrandHandler(BaseHandler):

    def __init__(self, repository: CarBrandRepository, storage: StorageService):
        super().__init__(repository)
        self.storage: StorageService = storage
        self.repository: CarBrandRepository = repository

    async def send_to_queue_for_create(
        self,
        data: CarBrandCreate,
        file: UploadFile,
    ):
        car_brand: CarBrand = await self.repository.get_by_name(name=data.name)

        if car_brand:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail=f"Марка {data.name} уже существует.",
            )

        self.__validate_file_extension(file=file)

        file_bytes: bytes = await file.read()
        file_base64 = base64.b64encode(file_bytes).decode("utf-8")
        msg = CarBrandCreateMessage(
            car_brand_data=data.model_dump(exclude_unset=True),
            file=file_base64,
        )
        await broker.publish(
            message=msg,
            queue="brand_create",
            content_type="application/json",
        )

    async def send_to_queue_for_update(
        self,
        car_brand_id: UUID,
        data: CarBrandUpdate,
        file: Optional[UploadFile],
    ):
        car_brand: CarBrand = await self.repository.get_by_id(id=car_brand_id)

        if not car_brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Марка {data.name} не найдена.",
            )
        file_base64 = None

        if file:
            self.__validate_file_extension(file=file)
            file_bytes: bytes = await file.read()
            file_base64 = base64.b64encode(file_bytes).decode("utf-8")

        msg = CarBrandUpdateMessage(
            car_brand_id=car_brand_id,
            car_brand_data=data.model_dump(exclude_unset=True),
            file=file_base64,
        )

        await broker.publish(
            message=msg,
            queue="brand_update",
            content_type="application/json",
        )

    async def create_car_brand(
        self,
        car_brand_data: dict,
        file: bytes,
    ):
        filename: str = await self.storage.create_file(file=file)
        car_brand_data.update({"picture": filename})

        brand: CarBrand | None = await self.repository.create(data=car_brand_data)
        if not brand:
            await self.storage.delete_file(filename=filename)
            raise Exception

    async def update_car_brand(
        self,
        car_brand_id: UUID,
        car_brand_data: dict,
        file: bytes | None,
    ):
        car_brand: CarBrand = await self.repository.get_by_id(id=car_brand_id)
        if file:
            filename: str = await self.storage.create_file(file=file)
            car_brand_data.update({"file": filename})

        updated_brand: CarBrand | None = await self.repository.update_by_id(
            id=car_brand_id,
            data=car_brand_data,
        )
        if not updated_brand:
            await self.storage.delete_file(filename=filename)
            raise Exception

        await self.storage.delete_file(filename=car_brand.picture)

    async def delete_car_brand(
        self,
        car_brand_id: UUID,
    ) -> bool:
        brand: CarBrand | None = await self.repository.get_by_id(id=car_brand_id)
        if not brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Марка {car_brand_id} не найдена.",
            )

        await self.storage.delete_file(brand.picture)
        result: bool = await self.repository.delete_by_id(id=car_brand_id)
        return result

    async def get_all_brands(
        self,
        query: str,
        page: int,
        page_size: int,
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

    def __validate_file_extension(self, file: UploadFile) -> None:
        allowed_formats = [
            "image/jpeg",
            "application/octet-stream",
            "image/png",
            "image/webp",
        ]

        if file.content_type not in allowed_formats:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail=f"Неверный формат файла. Приемлимые форматы файлов - {allowed_formats}. Был дан {file.content_type}.",
            )
