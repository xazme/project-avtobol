from typing import Optional
from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .product_repository import ProductRepository
from .product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductFilters,
)
from .product_model import Product


class ProductHandler(BaseHandler):

    def __init__(self, repository: ProductRepository):
        super().__init__(repository)
        self.repository: ProductRepository = repository

    async def create_product(
        self,
        product_data: ProductCreate,
    ) -> Optional[Product]:
        data = product_data.model_dump(exclude_unset=True)

        new_product: Product | None = await self.repository.create(data=data)

        if not new_product:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Ошибка во время создания продукта",
            )
        return new_product

    async def update_product(
        self,
        product_id: UUID,
        product_data: ProductUpdate,
    ) -> Optional[Product]:
        product: Product = await self.repository.get_by_id(id=product_id)

        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Продукт не найден.",
            )

        updated_product: Product | None = await self.repository.update_by_id(
            id=product_id,
            data=product_data.model_dump(exclude_unset=True),
        )

        if not updated_product:
            ExceptionRaiser.raise_exception(
                status_code=500,
                detail="Ошибка обновления продукта.",
            )

        return updated_product

    async def delete_product(
        self,
        product_id: UUID,
    ) -> bool:
        product: Product = await self.repository.get_by_id(id=product_id)
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Продукт {product_id} не найден.",
            )
        result: bool = await self.repository.delete_by_id(id=product_id)
        return result

    async def get_product_by_id(self, product_id: UUID) -> Optional[Product]:
        product: Product | None = await self.repository.get_product_by_id(id=product_id)
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Продукт {product_id} не найден.",
            )
        return product

    async def get_all_products(
        self,
        page: int,
        page_size: int,
        filters: ProductFilters,
    ) -> tuple[list[Product], int]:
        return await self.repository.get_all_products(
            page=page,
            page_size=page_size,
            filters=filters,
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
                status_code=500,
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
