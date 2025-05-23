from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from app.storage import get_storage_service
from .product_model import Product
from .product_repository import ProductRepository
from .product_handler import ProductHandler


def get_product_handler(
    session: AsyncSession = Depends(DBService.get_session),
    storage=Depends(get_storage_service),
):
    repository = ProductRepository(
        session=session,
        model=Product,
    )
    return ProductHandler(
        repository=repository,
        storage=storage,
    )
