from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import APIRouter, Path, Body, Depends, status
from app.user import UserRoles
from app.auth import requied_roles
from app.car.product import get_product_handler
from app.core import settings
from .cart_dependencies import get_cart_handler
from .cart_schema import CartResponse, CartResponseExtended
from .cart_helper import (
    convert_data_for_many_positions_in_cart,
)

router = APIRouter(
    prefix=settings.api.cart_prefix,
    tags=["Cart"],
)

if TYPE_CHECKING:
    from app.user import User
    from app.car.product import ProductHandler
    from .cart_handler import CartHandler


@router.post(
    "/items",
    summary="Add item to cart",
    description="Add a product to the user's shopping cart",
    status_code=status.HTTP_201_CREATED,
    response_model=CartResponse,
)
async def add_cart_item(
    product_id: UUID = Body(...),
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    cart_handler: "CartHandler" = Depends(get_cart_handler),
    product_handler: "ProductHandler" = Depends(get_product_handler),
):
    await product_handler.check_availability(product_id=product_id)
    position = await cart_handler.create_position(
        user_id=user.id, product_id=product_id
    )
    return CartResponse.model_validate(position)


@router.get(
    "/",
    summary="Get user cart",
    description="Retrieve all items in the current user's shopping cart",
    status_code=status.HTTP_200_OK,
    response_model=list[CartResponseExtended],
)
async def get_user_cart(
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    cart_handler: "CartHandler" = Depends(get_cart_handler),
) -> list[CartResponseExtended]:
    cart = await cart_handler.get_all_user_positions(user_id=user.id)
    return convert_data_for_many_positions_in_cart(list_of_positions=cart)


@router.delete(
    "/items/{product_id}",
    summary="Remove item from cart",
    description="Remove a specific product from the user's shopping cart",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def remove_cart_item(
    product_id: UUID = Path(...),
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    cart_handler: "CartHandler" = Depends(get_cart_handler),
) -> None:
    await cart_handler.delete_position(
        user_id=user.id,
        product_id=product_id,
    )


@router.delete(
    "/items",
    summary="Clear cart",
    description="Remove all items from the user's shopping cart",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def clear_cart(
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    cart_handler: "CartHandler" = Depends(get_cart_handler),
) -> None:
    await cart_handler.delete_all_positions(user_id=user.id)
