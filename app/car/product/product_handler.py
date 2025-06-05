from typing import Optional
from uuid import UUID
from fastapi import UploadFile
from app.shared import BaseHandler, ExceptionRaiser
from app.storage import StorageService
from app.faststream import broker
from .product_repository import ProductRepository
from .product_schema import ProductCreate, ProductUpdate, ProductFilters
from .product_model import Product


class ProductHandler(BaseHandler):

    def __init__(self, repository: ProductRepository, storage: StorageService):
        super().__init__(repository)
        self.storage: StorageService = storage
        self.repository: ProductRepository = repository

    async def send_to_queue(
        self,
        data: ProductCreate,
        files: list[UploadFile],
    ):
        allowed_formats = [
            "image/jpeg",
            "application/octet-stream",
            "image/png",
            "image/webp",
        ]
        for file in files:
            if file.content_type not in allowed_formats:
                ExceptionRaiser.raise_exception(
                    status_code=400,
                    detail=f"Wrong file extension. Allowed formats - {allowed_formats}. Get {file.content_type}",
                )
        file_contents: list[bytes] = [await file.read() for file in files]
        msg: dict = {
            "product_data": data.model_dump(exclude_unset=True),
            "pictures": file_contents,
        }
        await broker.publish(
            message=msg,
            queue="product_input",
            content_type="application/json",
        )

    async def create_product(
        self,
        msg: dict,
    ) -> Optional[Product]:
        product = msg.copy()
        filenames: list[str] = await self.storage.create_files(
            list_of_files=product["pictures"]
        )
        product.update({"pictures": filenames})
        new_product: Product | None = await self.repository.create(data=product)

        if not new_product:
            await self.storage.delete_files(list_of_files=filenames)
        return new_product

    async def update_product(
        self,
        product_id: UUID,
        new_data: ProductUpdate,
        files: Optional[list[UploadFile]],
    ) -> Optional[Product]:
        old_product: dict = await self.get_product_by_id(product_id)
        file_contents: list[bytes] = []
        filenames: list[str] = old_product["pictures"]

        if files:
            allowed_formats = [
                "image/jpeg",
                "application/octet-stream",
                "image/png",
                "image/webp",
            ]
            for file in files:
                if file.content_type not in allowed_formats:
                    ExceptionRaiser.raise_exception(
                        status_code=400,
                        detail=f"Wrong file extension. Allowed formats - {allowed_formats}. Get {file.content_type}",
                    )
            for file in files:
                file_contents.append(await file.read())
            filenames = await self.storage.create_files(list_of_files=file_contents)

        product: dict = new_data.model_dump(exclude_unset=True)

        if filenames:
            product.update({"pictures": filenames})

        upd_product: Product | None = await self.repository.update_by_id(
            id=product_id, data=product
        )
        if not upd_product:
            ExceptionRaiser.raise_exception(
                status_code=500,
                detail="We can't update this product.",
            )
        if files:
            await self.storage.delete_files(list_of_files=old_product["pictures"])
        return upd_product

    async def change_availability(
        self,
        product_id: UUID,
        new_status: bool,
    ) -> dict:
        product: Product | None = await self.repository.change_availibility(
            product_id=product_id,
            new_available_status=new_status,
        )
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=500, detail="Product update failed."
            )
        return product

    async def delete_product(
        self,
        product_id: UUID,
    ) -> bool:
        return await self.delete_obj(id=product_id)

    async def get_product_by_id(self, product_id: UUID) -> Optional[Product]:
        product: Product | None = await self.repository.get_product_by_id(id=product_id)
        if not product:
            ExceptionRaiser.raise_exception(
                status_code=404,
                detail="Product not found.",
            )
        return product

    async def get_all_products(
        self,
        page: int,
        page_size: int,
        filters: ProductFilters,
    ) -> list[Product]:
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
                status_code=400, detail="Product is not available for sale."
            )
        return result
