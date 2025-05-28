from uuid import UUID
from app.shared import BaseHandler, ExceptionRaiser
from .cart_repository import CartRepository
from .cart_schema import CartCreate


class CartHandler(BaseHandler):
    def __init__(
        self,
        repository: CartRepository,
    ):
        super().__init__(repository)
        self.repository = repository

    async def get_all_user_positions(
        self,
        user_id: UUID,
    ):
        return await self.repository.get_all_user_positions(user_id=user_id)

    async def create_position(
        self,
        user_id: UUID,
        data: CartCreate,
    ):
        position_data = data.model_copy(update={"user_id": user_id})
        obj = await self.repository.create_position(
            position_data=position_data.model_dump(exclude_unset=True)
        )
        if not obj:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail=f"Такого товара не существует, либо он в вашей корзине",
            )
        return obj

    async def delete_position(
        self,
        user_id: UUID,
        position_id: UUID,
    ):
        result = await self.repository.delete_position(
            user_id=user_id,
            position_id=position_id,
        )
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail=f"Failed to delete a obj {position_id}. Location - {self.__class__.__name__}",
            )
        return result

    async def delete_all_positions(
        self,
        user_id: UUID,
    ):
        result = await self.repository.delete_all_positions(user_id=user_id)
        return result
