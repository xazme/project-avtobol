from pydantic import BaseModel
from app.shared import BaseHandler, ExceptionRaiser
from .cart_repository import CartRepository


class CartHandler(BaseHandler):
    def __init__(self, repository):
        super().__init__(repository)
        self.repository: CartRepository = repository

    async def get_all_user_positions(
        self,
        user_id: int,
    ):
        return await self.repository.get_all_positions(user_id=user_id)

    async def add_position(
        self,
        user_id: int,
        data: BaseModel,
    ):
        data = data.model_copy(update={"user_id": user_id})
        obj = await self.repository.add_position(
            data=data.model_dump(exclude_unset=True),
        )
        if not obj:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail=f"Такого товара не существует, либо он в вашей корзине",
            )
        return obj

    async def delete_position(self, position_id: int, user_id: int):
        result = await self.repository.delete_position(
            position_id=position_id, user_id=user_id
        )
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail=f"Failed to delete a obj {position_id}. Location - {self.__class__.__name__}",
            )
        return result

    async def delete_all_positions(self, user_id: int):
        result = await self.repository.delete_all_positions(user_id=user_id)
        if not result:
            ExceptionRaiser.raise_exception(
                status_code=409,
                detail=f"Корзина пуста",
            )
        return result
