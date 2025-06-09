from typing import Optional
from uuid import UUID
from app.shared import ExceptionRaiser, BaseHandler
from .car_brand_schema import (
    CarBrandCreate,
    CarBrandUpdate,
)
from .car_brand_repository import CarBrandRepository
from .car_brand_model import CarBrand


class CarBrandHandler(BaseHandler):

    def __init__(self, repository: CarBrandRepository):
        super().__init__(repository)
        self.repository: CarBrandRepository = repository

    async def create_car_brand(
        self,
        car_brand_data: CarBrandCreate,
    ) -> Optional[CarBrand]:
        car_brand: CarBrand = await self.repository.get_by_name(
            name=car_brand_data.name
        )

        if car_brand:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail=f"Марка {car_brand_data.name} уже существует.",
            )

        car_brand_data_dict: dict = car_brand_data.model_dump(exclude_unset=True)

        new_brand: CarBrand | None = await self.repository.create(
            data=car_brand_data_dict
        )

        if not new_brand:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Ошибка во время создания марки.",
            )

        return new_brand

    async def update_car_brand(
        self,
        car_brand_id: UUID,
        car_brand_data: CarBrandUpdate,
    ) -> Optional[CarBrand]:
        car_brand: CarBrand = await self.repository.get_by_id(id=car_brand_id)

        if not car_brand:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail=f"Марка {car_brand_id} не существует.",
            )

        upd_car_brand_data_dict: dict = car_brand_data.model_dump(exclude_unset=True)

        updated_brand: CarBrand | None = await self.repository.update_by_id(
            id=car_brand_id,
            data=upd_car_brand_data_dict,
        )

        if not updated_brand:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Ошибка во время обновления марки.",
            )

        return updated_brand

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
