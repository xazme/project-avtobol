from typing import Optional
from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .product_repository import ProductRepository
from .product_schema import (
    ProductFiltersPublic,
    ProductFiltersPrivate,
)
from .product_model import Product
from ..tire.tire import TireFiltersPublic, TireFiltersPrivate
from ..disc.disc import DiscFiltersPublic, DiscFiltersPrivate
from ..engine import EngineFilters


class ProductHandler(BaseHandler):

    def __init__(
        self,
        repository: ProductRepository,
    ):
        super().__init__(repository)
        self.repository: ProductRepository = repository

    async def get_product_by_id(
        self,
        product_id: UUID,
    ) -> Optional[Product]:
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

    async def get_all_products_by_page(
        self,
        page: int,
        page_size: int,
        product_filters: ProductFiltersPublic | ProductFiltersPrivate | None,
        tire_filters: TireFiltersPublic | TireFiltersPrivate | None,
        disc_filters: DiscFiltersPublic | DiscFiltersPrivate | None,
        engine_filters: EngineFilters | None,
    ) -> tuple[int, list[Product]]:
        return await self.repository.get_all_products_by_page(
            page=page,
            page_size=page_size,
            product_filters=product_filters,
            tire_filters=tire_filters,
            disc_filters=disc_filters,
            engine_filters=engine_filters,
        )

    async def get_all_products_by_cursor(
        self,
        cursor: int | None,
        take: int | None,
        product_filters: ProductFiltersPublic | ProductFiltersPrivate | None,
        tire_filters: TireFiltersPublic | TireFiltersPrivate | None,
        disc_filters: DiscFiltersPublic | DiscFiltersPrivate | None,
        engine_filters: EngineFilters | None,
    ) -> tuple[int, int, list[Product]]:
        return await self.repository.get_all_products_by_cursor(
            cursor=cursor,
            take=take,
            product_filters=product_filters,
            tire_filters=tire_filters,
            disc_filters=disc_filters,
            engine_filters=engine_filters,
        )

    async def check_availability(
        self,
        product_id: UUID,
    ) -> bool:
        is_available: bool = await self.repository.check_availability(
            product_id=product_id
        )
        if not is_available:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Продукт недоступен для продажи.",
            )
        return is_available

    async def bulk_update_availability(
        self,
        products_id: list[UUID],
        new_status: bool,
    ) -> list[Product]:
        products: list[Product] | None = await self.repository.bulk_update_availibility(
            products_id=products_id,
            new_availables_status=new_status,
        )
        if not products:
            ExceptionRaiser.raise_exception(
                status_code=422,
                detail="Не удалось обновить доступность продуктов.",
            )
        return products

    async def bulk_update_printed_status(
        self,
        products_id: list[UUID],
        status: bool,
    ) -> list[Product]:
        products: list[Product] | None = (
            await self.repository.bulk_update_printed_status(
                products_id=products_id,
                status=status,
            )
        )
        if not products:
            ExceptionRaiser.raise_exception(
                status_code=422,
                detail="Не удалось обновить доступность продуктов.",
            )
        return products

    async def update_product_availability(
        self,
        product_id: UUID,
        status: bool,
    ) -> Product:
        product: Product | None = await self.repository.update_product_availability(
            product_id=product_id,
            status=status,
        )
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail="Не удалось обновить доступность продукта.",
            )
        return product
