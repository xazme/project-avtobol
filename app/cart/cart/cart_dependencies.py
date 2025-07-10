from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import DBService
from .cart_repository import CartRepository
from .cart_handler import CartHandler
from .cart_model import Cart


def get_cart_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> CartHandler:
    repository = CartRepository(session=session, model=Cart)
    return CartHandler(repository=repository)
