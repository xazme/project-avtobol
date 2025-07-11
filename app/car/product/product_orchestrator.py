from uuid import UUID
from typing import TYPE_CHECKING
from fastapi import UploadFile
from pydantic import BaseModel
from app.shared import ExceptionRaiser, BaseCRUD
from app.storage import StorageHandler
from .product_schema import ProductCreate, ProductUpdate
from .product_handler import ProductHandler
from ..disc.disc import DiscHandler
from ..tire.tire import TireHandler
from ..engine import EngineHandler

if TYPE_CHECKING:
    from .product_model import Product
    from ..disc.disc import Disc
    from ..tire.tire import Tire
    from ..engine import Engine


class ProductOrchestrator:
    def __init__(
        self,
        product_handler: ProductHandler,
        disc_handler: DiscHandler,
        tire_handler: TireHandler,
        engine_handler: EngineHandler,
        storage_handler: StorageHandler,
    ):
        self.product_handler: ProductHandler = product_handler
        self.disc_handler: DiscHandler = disc_handler
        self.tire_handler: TireHandler = tire_handler
        self.engine_handler: EngineHandler = engine_handler
        self.storage_handler: StorageHandler = storage_handler

    async def create_product(
        self,
        user_id: UUID,
        product_data: ProductCreate,
        files: list[UploadFile],
    ) -> "Product":
        tire_data = product_data.tire
        disc_data = product_data.disc
        engine_data = product_data.engine

        main_product_data = product_data.model_dump(
            exclude_unset=True,
            exclude={"tire", "disc", "engine"},
        )

        main_product_data.update({"post_by": user_id})

        file_bytes = await self.__validate_files(files=files)
        filenames = await self.storage_handler.create_files(list_of_files=file_bytes)
        main_product_data.update({"pictures": filenames})

        product: "Product" | None = (
            await self.product_handler.repository.create_product(
                data=main_product_data,
            )
        )

        if not product:
            await self.storage_handler.delete_files(list_of_files=filenames)
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Ошибка во время создания продукта.",
            )

        product_id = product.id

        if tire_data:
            data = self.__connect_product_with_car_part(
                car_part_data=tire_data,
                product_id=product_id,
            )
            tire: "Tire" | None = await self.tire_handler.repository.create(data=data)
            if not tire:
                ExceptionRaiser.raise_exception(
                    status_code=400,
                    detail=f"Неудалось создать продукт. Ошибка создания {tire_data}",
                )
        if disc_data:
            data = self.__connect_product_with_car_part(
                car_part_data=disc_data,
                product_id=product_id,
            )
            disc: "Disc" | None = await self.disc_handler.repository.create(
                data=data,
            )
            if not disc:
                await self.delete_product(product_id=product_id)
                ExceptionRaiser.raise_exception(
                    status_code=400,
                    detail=f"Неудалось создать продукт. Ошибка создания {disc_data}",
                )
        if engine_data:
            data = self.__connect_product_with_car_part(
                car_part_data=engine_data,
                product_id=product_id,
            )
            engine: "Engine" | None = await self.engine_handler.repository.create(
                data=data,
            )
            if not engine:
                await self.delete_product(product_id=product_id)
                ExceptionRaiser.raise_exception(
                    status_code=400,
                    detail=f"Неудалось создать продукт. Ошибка создания {engine_data}",
                )

        return product

    async def update_product(
        self,
        product_id: UUID,
        user_id: UUID,
        product_data: ProductUpdate,
        new_photos: list[UploadFile] | None = None,
        removed_photos: list[str] | None = None,
    ) -> "Product":
        product: "Product" = await self.product_handler.repository.get_by_id(
            id=product_id
        )
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Продукт не найден.",
            )

        current_photos = product.pictures or []

        if product_data.pictures is not None:
            invalid_photos = [
                p for p in product_data.pictures if p not in current_photos
            ]
            if invalid_photos:
                ExceptionRaiser.raise_exception(
                    status_code=400,
                    detail=f"Неверные имена фотографий: {', '.join(invalid_photos)}",
                )

            requested_deletions = set(current_photos) - set(product_data.pictures)
            if removed_photos and requested_deletions - set(removed_photos):
                ExceptionRaiser.raise_exception(
                    status_code=400,
                    detail="Несогласованное удаление фотографий",
                )

            effective_removals = list(set(removed_photos or []) | requested_deletions)
        else:
            effective_removals = removed_photos or []
            product_data.pictures = current_photos

        data = product_data.model_dump(
            exclude_unset=True,
            exclude={"tire", "disc", "engine"},
        )
        data.update({"post_by": user_id})

        new_filenames = []
        if new_photos:
            file_bytes = await self.__validate_files(files=new_photos)
            new_filenames = await self.storage_handler.create_files(
                list_of_files=file_bytes,
            )
            data.update({"pictures": product_data.pictures + new_filenames})

        if removed_photos:
            updated_photos = [
                p
                for p in data.get("pictures", current_photos)
                if p not in effective_removals
            ]
            data.update({"pictures": updated_photos})

        updated_product = await self.product_handler.repository.update_by_id(
            id=product_id,
            data=data,
        )

        if not updated_product:
            if new_filenames:
                await self.storage_handler.delete_files(list_of_files=new_filenames)
            ExceptionRaiser.raise_exception(
                status_code=422,
                detail="Ошибка обновления продукта.",
            )

        if effective_removals:
            await self.storage_handler.delete_files(list_of_files=effective_removals)

        if product_data.tire:
            tire_data = self.__connect_product_with_car_part(
                car_part_data=product_data.tire,
                product_id=product_id,
            )
            await self.tire_handler.repository.update_or_create(
                product_id=product_id,
                data=tire_data,
            )

        if product_data.disc:
            disc_data = self.__connect_product_with_car_part(
                car_part_data=product_data.disc,
                product_id=product_id,
            )
            await self.disc_handler.repository.update_or_create(
                product_id=product_id,
                data=disc_data,
            )

        if product_data.engine:
            engine_data = self.__connect_product_with_car_part(
                car_part_data=product_data.engine,
                product_id=product_id,
            )
            await self.engine_handler.repository.update_or_create(
                product_id=product_id,
                data=engine_data,
            )

        return updated_product

    async def delete_product(
        self,
        product_id: UUID,
    ) -> None:
        product: Product = await self.product_handler.repository.get_product_by_id(
            id=product_id,
        )
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Продукт {product_id} не найден.",
            )
        tire = product.tire
        disc = product.disc
        engine = product.engine

        if tire:
            await self.tire_handler.delete_obj(id=tire.id)
        if disc:
            await self.disc_handler.delete_obj(id=disc.id)
        if engine:
            await self.engine_handler.delete_obj(id=engine.id)

        result = await self.product_handler.repository.delete_by_id(id=product_id)
        if result and product.pictures:
            await self.storage_handler.delete_files(list_of_files=product.pictures)

    def __connect_product_with_car_part(
        self,
        car_part_data: BaseModel,
        product_id: UUID,
    ) -> dict:
        data = car_part_data.model_dump(exclude_unset=True)
        data.update({"product_id": product_id})
        return data

    async def __validate_files(
        self,
        files: list[UploadFile],
    ) -> list[bytes]:
        self.__validate_files_extension(files=files)
        file_bytes = await self.__get_file_bytes(files=files)
        return file_bytes

    def __validate_files_extension(
        self,
        files: list[UploadFile],
    ) -> None:
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

    async def __get_file_bytes(
        self,
        files: list[UploadFile],
    ) -> list[bytes]:
        try:
            file_bytes = []
            for file in files:
                file_bytes.append(await file.read())
        except Exception:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Не удалось прочитать файлы.",
            )
        return file_bytes
