from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import APIRouter, status, Depends
from app.user import UserRoles
from app.auth import requied_roles
from app.car.product import get_product_handler
from .cart_dependencies import get_cart_handler
from .cart_schema import CartResponse
from .cart_helper import convert_data_for_cart

router = APIRouter(prefix="/cart")

if TYPE_CHECKING:
    from app.user import User
    from app.car.product import ProductHandler
    from .cart_handler import CartHandler


@router.get("/")
async def get_user_cart(
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    cart_handler: "CartHandler" = Depends(get_cart_handler),
):
    cart = await cart_handler.get_all_user_positions(user_id=user.id)
    return convert_data_for_cart(cart)


@router.post("/")
async def add_position(
    product_id: UUID,
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    cart_handler: "CartHandler" = Depends(get_cart_handler),
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    await product_handler.check_availability(product_id=product_id)
    position = await cart_handler.create_position(
        user_id=user.id, product_id=product_id
    )
    return CartResponse.model_validate(position)


@router.delete("/d")
async def delete_position(
    product_id: UUID,
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    cart_handler: "CartHandler" = Depends(get_cart_handler),
):
    await cart_handler.delete_position(
        user_id=user.id,
        product_id=product_id,
    )
    return {"msg": "success"}


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
)
async def delete_all_positions(
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    cart_handler: "CartHandler" = Depends(get_cart_handler),
):
    await cart_handler.delete_all_positions(user_id=user.id)
    return {"msg": "success"}
