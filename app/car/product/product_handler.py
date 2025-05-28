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
        product = data.model_dump(exclude_unset=True)
        product.update({"pictures": filenames})
        new_product = await self.repository.create(
            data=product,
        )

        if not new_product:
            await self.storage.delete_files(list_of_files=filenames)
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="We can create this product",
            )
        return new_product

    async def update_product(
        self,
        product_id: UUID,
        new_data: ProductUpdate,
        files: list[UploadFile] | None,
    ):
        old_product = await self.get_product_by_id(id=product_id)
        file_contents = []
        filenames = old_product.pictures

        if files:
            for file in files:
                file_contents.append(await file.read())
            filenames = await self.storage.create_files(list_of_files=file_contents)

        product = new_data.model_dump(exclude_unset=True)
        product.update({"pictures": filenames})

        upd_product = await self.repository.update_by_id(
            id=product_id,
            data=product,
        )
        if not upd_product:
            ExceptionRaiser.raise_exception(
                status_code=500,
                detail="We cant update this product",
            )
        if files:
            await self.storage.delete_files(list_of_files=old_product.pictures)
        return upd_product

    async def change_availability(
        self,
        product_id: UUID,
        new_status: bool,
    ):
        product = await self.repository.change_availibility(
            product_id=product_id,
            new_available_status=new_status,
        )
        if not product:
            ExceptionRaiser.raise_exception(status_code=500, detail="no")
        return product

    async def delete_product(
        self,
        product_id: UUID,
    ):
        return await super().delete_obj(id=product_id)

    async def get_product_by_id(
        self,
        product_id: UUID,
    ):
        product = await self.repository.get_product_by_id(id=product_id)
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Not Found",
            )
        return product

    async def get_all_products(self, page: int, page_size: int):
        return await self.repository.get_all_products(
            page=page,
            page_size=page_size,
        )
