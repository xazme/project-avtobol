from uuid import UUID
from pydantic import BaseModel
from app.shared import BaseHandler, ExceptionRaiser
from .cart_repository import CartRepository


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
        user_id: int,
        data: BaseModel,
    ):
        position_data = data.model_dump(exclude_unset=True)
        obj = await self.repository.create_position(
            user_id=user_id,
            **position_data,
        )
        if not obj:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail=f"Такого товара не существует, либо он в вашей корзине",
            )
        return obj

    async def delete_position(
        self,
        user_id: int,
        position_id: int,
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

    async def delete_all_positions(self, user_id: int):
        result = await self.repository.delete_all_positions(user_id=user_id)
        return result
