from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .bucket_repository import BucketRepository
from .bucket_handler import BucketHandler


def get_cart_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> BucketHandler:
    repository = BucketRepository(session=session)
    return BucketHandler(repository=repository)
