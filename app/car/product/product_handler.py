from typing import Optional
from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .product_repository import ProductRepository
from .product_schema import (
    ProductFilters,
    ProductFiltersExtended,
)
from .product_model import Product
from ..tire.tire import TireFilters
from ..disc.disc import DiscFilters
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

    async def get_all_products(
        self,
        is_private: bool,
        page: int,
        page_size: int,
        main_filters: ProductFilters | ProductFiltersExtended | None,
        tire_filters: TireFilters | None,
        disc_filters: DiscFilters | None,
        engine_filters: EngineFilters | None,
    ) -> tuple[list[Product], int]:
        return await self.repository.get_all_products(
            page=page,
            page_size=page_size,
            main_filters=main_filters,
            tire_filters=tire_filters,
            disc_filters=disc_filters,
            engine_filters=engine_filters,
            is_private=is_private,
        )

    async def get_all_products_by_scroll(
        self,
        cursor: int | None,
        take: int | None,
        is_private: bool,
        main_filters: ProductFilters | ProductFiltersExtended | None,
        tire_filters: TireFilters | None,
        disc_filters: DiscFilters | None,
        engine_filters: EngineFilters | None,
    ):
        return await self.repository.get_all_products_by_scroll(
            cursor=cursor,
            take=take,
            is_private=is_private,
            main_filters=main_filters,
            tire_filters=tire_filters,
            disc_filters=disc_filters,
            engine_filters=engine_filters,
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
    ) -> bool:
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
                detail="Неудалось обновить доступность продукта.",
            )
        return product

    async def bulk_change_printed_status(
        self,
        products_id: list[UUID],
        status: bool,
    ):
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
