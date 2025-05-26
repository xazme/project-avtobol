from uuid import UUID
from fastapi import UploadFile
from app.shared import BaseHandler, ExceptionRaiser
from app.storage import StorageService
from .product_repository import ProductRepository
from .product_schema import ProductCreate, ProductUpdate


class ProductHandler(BaseHandler):

    def __init__(
        self,
        repository: ProductRepository,
        storage: StorageService,
    ):
        super().__init__(repository)
        self.storage = storage
        self.repository = repository

    async def create_product(
        self,
        data: ProductCreate,
        files: list[UploadFile],
    ):
        files = [await file.read() for file in files]
        filenames = await self.storage.create_files(list_of_files=files)
        car_part = data.model_dump(exclude_unset=True)
        car_part.update({"pictures": filenames})
        product = await self.repository.create(
            data=car_part,
        )

        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="We can create this product",
            )
        return product

    async def update_product(
        self,
        id: UUID,
        data: ProductUpdate,
    ):
        return await super().update_obj(id, data)

    async def delete_product(
        self,
        id: UUID,
    ):
        return await super().delete_obj(id)

    async def get_product_by_id(
        self,
        id: UUID,
    ):
        product = await self.repository.get_product_by_id(id=id)
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Not Found",
            )
        return product

    async def get_all_products(self):
        return await self.repository.get_all_products()
