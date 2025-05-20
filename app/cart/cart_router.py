from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends
from app.security import requied_roles
from app.shared import Roles
from .cart_dependencies import get_cart_handler
from .cart_schema import CartResponse, CartCreate

router = APIRouter("/cart")

if TYPE_CHECKING:
    from .cart_handler import CartHandler
    from app.user import User


@router.get("/")
async def get_user_cart(
    user: "User" = Depends(requied_roles([Roles.CLIENT])),
    cart_handler: "CartHandler" = Depends(get_cart_handler),
):
    cart = await cart_handler.get_positions(user_id=user.id)
    return [CartResponse.model_validate(position) for position in cart]


@router.post("/")
async def add_position(
    cart_data: CartCreate,
    user: "User" = Depends(requied_roles([Roles.CLIENT])),
    cart_handler: "CartHandler" = Depends(get_cart_handler),
):
    position = await cart_handler.add_position(cart_data, user_id=user.id)
    return CartResponse.model_validate(position)


@router.delete("/")
async def delete_position(
    position_id: int,
    user: "User" = Depends(requied_roles([Roles.CLIENT])),
    cart_handler: "CartHandler" = Depends(get_cart_handler),
):
    result = await cart_handler.delete_position(id=id)
    return {"msg": "success"}


@router.delete("/")
async def delete_all_positions(
    user: "User" = Depends(requied_roles([Roles.CLIENT])),
    cart_handler: "CartHandler" = Depends(get_cart_handler),
):
    result = await cart_handler.delete_all_positions(user_id=user.id)
    return {"msg": "success"}
