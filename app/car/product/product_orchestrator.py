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
        # Получаем текущий продукт
        product: Product = await self.product_handler.repository.get_by_id(
            id=product_id
        )
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Продукт не найден.",
            )

        # Текущий список фотографий у продукта
        existing_photos: list[str] = product.pictures or []

        # Список, который передал фронт (итоговый порядок фотографий)
        requested_photos: list[str] = product_data.pictures or []

        # Проверка: фронт указал несуществующие фото?
        invalid_photo_names = [
            photo_name
            for photo_name in requested_photos
            if photo_name not in existing_photos
        ]
        if invalid_photo_names:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail=f"Неверные имена фотографий: {', '.join(invalid_photo_names)}",
            )

        # Фото, которые были в продукте, но исчезли из списка — фронт хочет их удалить
        photos_removed_by_diff = set(existing_photos) - set(requested_photos)

        # Проверка согласованности: если переданы removed_photos, они должны содержать всё, что удалено
        if removed_photos:
            explicitly_removed_photos = set(removed_photos)
            if not photos_removed_by_diff.issubset(explicitly_removed_photos):
                ExceptionRaiser.raise_exception(
                    status_code=400,
                    detail="Несогласованное удаление фотографий.",
                )
        else:
            removed_photos = list(photos_removed_by_diff)

        # Загрузка новых фотографий, если переданы
        new_photo_filenames: list[str] = []
        if new_photos:
            validated_file_contents = await self.__validate_files(files=new_photos)
            new_photo_filenames = await self.storage_handler.create_files(
                validated_file_contents
            )

            # Проверка на конфликт имён
            conflicting_names = set(new_photo_filenames) & set(existing_photos)
            if conflicting_names:
                ExceptionRaiser.raise_exception(
                    status_code=400,
                    detail=f"Конфликт имён: новые фото уже существуют: {', '.join(conflicting_names)}",
                )

        # Финальный список фото: оставшиеся старые (без удалённых) + новые
        final_photo_list: list[str] = [
            photo_name
            for photo_name in existing_photos
            if photo_name not in removed_photos
        ] + new_photo_filenames

        # Формируем данные для обновления
        update_data: dict = product_data.model_dump(
            exclude_unset=True,
            exclude={"tire", "disc", "engine"},
        )
        update_data.update(
            {
                "pictures": final_photo_list,
                "post_by": user_id,
            }
        )

        # Обновляем продукт в БД
        updated_product = await self.product_handler.repository.update_by_id(
            id=product_id,
            data=update_data,
        )

        # Если обновление не удалось — удаляем загруженные новые файлы
        if not updated_product:
            if new_photo_filenames:
                await self.storage_handler.delete_files(
                    list_of_files=new_photo_filenames
                )
            ExceptionRaiser.raise_exception(
                status_code=422,
                detail="Ошибка обновления продукта.",
            )

        # Удаляем из хранилища файлы, которые явно удалил пользователь
        if removed_photos:
            await self.storage_handler.delete_files(list_of_files=removed_photos)

        # Обновление связанных сущностей: шина
        if product_data.tire:
            tire_data = self.__connect_product_with_car_part(
                car_part_data=product_data.tire,
                product_id=product_id,
            )
            await self.tire_handler.repository.update_or_create(
                product_id=product_id,
                data=tire_data,
            )

        # Диск
        if product_data.disc:
            disc_data = self.__connect_product_with_car_part(
                car_part_data=product_data.disc,
                product_id=product_id,
            )
            await self.disc_handler.repository.update_or_create(
                product_id=product_id,
                data=disc_data,
            )

        # Двигатель
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
