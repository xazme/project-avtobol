from typing import Optional
from uuid import UUID
from fastapi import UploadFile
from app.shared import BaseHandler, ExceptionRaiser
from app.storage import StorageHandler
from .product_repository import ProductRepository
from .product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductFilters,
)
from .product_model import Product


class ProductHandler(BaseHandler):

    def __init__(self, repository: ProductRepository, storage: StorageHandler):
        super().__init__(repository)
        self.repository: ProductRepository = repository
        self.storage: StorageHandler = storage

    async def create_product(
        self,
        user_id: UUID,
        product_data: ProductCreate,
        files: list[UploadFile],
    ) -> Product:
        self.__validate_files(files)

        try:
            file_bytes = [await f.read() for f in files]
        except Exception:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Не удалось прочитать файлы.",
            )

        filenames = await self.storage.create_files(list_of_files=file_bytes)
        data = product_data.model_dump(exclude_unset=True)
        data.update({"pictures": filenames})
        data.update({"post_by": user_id})

        new_product = await self.repository.create(data=data)
        if not new_product:
            await self.storage.delete_files(list_of_files=filenames)
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Ошибка во время создания продукта.",
            )

        return new_product

    async def update_product(
        self,
        product_id: UUID,
        user_id: UUID,
        product_data: ProductUpdate,
        files: list[UploadFile] | None,
    ) -> Product:
        product: Product = await self.repository.get_by_id(id=product_id)
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Продукт не найден.",
            )

        old_filenames = product.pictures or []
        data = product_data.model_dump(exclude_unset=True)
        new_filenames = []

        if files:
            self.__validate_files(files)
            try:
                file_bytes = [await f.read() for f in files]
            except Exception:
                ExceptionRaiser.raise_exception(
                    status_code=400,
                    detail="Не удалось прочитать файлы.",
                )

            new_filenames = await self.storage.create_files(list_of_files=file_bytes)
            data.update({"pictures": new_filenames})
            data.update({"post_by": user_id})

        updated_product = await self.repository.update_by_id(id=product_id, data=data)
        if not updated_product:
            if new_filenames:
                await self.storage.delete_files(list_of_files=new_filenames)
            ExceptionRaiser.raise_exception(
                status_code=422,
                detail="Ошибка обновления продукта.",
            )

        if new_filenames and old_filenames:
            await self.storage.delete_files(list_of_files=old_filenames)

        return updated_product

    async def delete_product(self, product_id: UUID) -> bool:
        product: Product = await self.repository.get_by_id(id=product_id)
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Продукт {product_id} не найден.",
            )

        result = await self.repository.delete_by_id(id=product_id)
        if result and product.pictures:
            await self.storage.delete_files(list_of_files=product.pictures)

        return result

    async def get_product_by_id(self, product_id: UUID) -> Optional[Product]:
        product: Product | None = await self.repository.get_product_by_id(id=product_id)
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Продукт {product_id} не найден.",
            )
        return product

    async def get_product_by_article(
        self,
        article: str,
    ) -> Optional[Product]:
        product: Product | None = await self.repository.get_product_by_article(
            article=article,
        )
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Продукт {article} не найден.",
            )
        return product

    async def get_all_products(
        self,
        is_private: bool,
        page: int,
        page_size: int,
        filters: ProductFilters,
    ) -> tuple[list[Product], int]:
        return await self.repository.get_all_products(
            page=page,
            page_size=page_size,
            filters=filters,
            is_private=is_private,
        )

    async def check_availability(
        self,
        product_id: UUID,
    ) -> bool:
        result: bool = await self.repository.check_availability(product_id=product_id)
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Продукт недоступен для продажи.",
            )
        return result

    async def bulk_change_availability(
        self,
        products_id: list[UUID],
        new_status: bool,
    ) -> dict:
        product: Product | None = await self.repository.bulk_change_availibility(
            products_id=products_id,
            new_availables_status=new_status,
        )
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=422,
                detail="Неудалось обновить продукт.",
            )
        return product

    async def bulk_change_printed_status(self, products_id: list[UUID], status: bool):
        result = await self.repository.bulk_change_printed_status(
            products_id=products_id,
            status=status,
        )
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=503,
                detail="Лок транзакции. Повторите попытку позже.",
            )
        return True

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
