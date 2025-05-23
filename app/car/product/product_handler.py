from pydantic import BaseModel
from fastapi import UploadFile
from app.shared import BaseHandler, ExceptionRaiser
from app.storage import StorageService
from .product_repository import ProductRepository


class ProductHandler(BaseHandler):
    def __init__(
        self,
        repository,
        storage: StorageService,
    ):
        super().__init__(repository)
        self.storage = storage
        self.repository: ProductRepository = repository

    async def create(
        self,
        data: BaseModel,
        files: list[bytes | UploadFile],
    ):
        filenames = await self.storage.create_files(list_of_files=files)
        car_part = data.model_dump(exclude_unset=True)
        car_part.update({"pictures": filenames})
        print(car_part)
        product = await self.repository.create(
            data=car_part,
        )

        # if not product:
        #     ExceptionRaiser.raise_exception(
        #         status_code=404,
        #         detail="We can create this product",
        #     )
        return product
