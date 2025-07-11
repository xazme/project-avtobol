from typing import TYPE_CHECKING
from fastapi import APIRouter, Body, Depends, status
from app.core import settings
from app.user.user_enums import UserRoles
from app.auth.auth_guard import required_roles
from .cart_item_schema import (
    CartAddItem,
    CartDeleteItem,
    CartItemResponse,
    CartItemResponseExtended,
)
from .cart_item_dependencies import get_cart_item_orchestrator
from .cart_item_helper import convert_cart_items

router = APIRouter(
    prefix=settings.api.cart_prefix,
    tags=["Cart"],
)

if TYPE_CHECKING:
    from app.user import User
    from .cart_item_orchestrator import CartItemOrchestrator


@router.post(
    "/items",
    summary="Add item to cart",
    description="Add a product to the user's shopping cart",
    status_code=status.HTTP_201_CREATED,
    response_model=CartItemResponse,
)
async def add_cart_item(
    item: CartAddItem = Body(...),
    user: "User" = Depends(required_roles(allowed_roles=[UserRoles.CLIENT])),
    cart_item_orchestrator: "CartItemOrchestrator" = Depends(
        get_cart_item_orchestrator
    ),
):
    item_in_the_cart = await cart_item_orchestrator.add_item(user_id=user.id, data=item)
    return CartItemResponse.model_validate(item_in_the_cart)


@router.get(
    "/",
    summary="Get user cart",
    description="Retrieve all items in the current user's shopping cart",
    status_code=status.HTTP_200_OK,
    response_model=list[CartItemResponseExtended],
)
async def get_user_cart(
    user: "User" = Depends(required_roles(allowed_roles=[UserRoles.CLIENT])),
    cart_item_orchestrator: "CartItemOrchestrator" = Depends(
        get_cart_item_orchestrator
    ),
) -> list[CartItemResponseExtended]:
    user_cart = await cart_item_orchestrator.get_user_cart(user_id=user.id)
    return convert_cart_items(cart_items=user_cart)


@router.delete(
    "/items/{product_id}",
    summary="Delete item from cart",
    description="Remove a specific product from the user's shopping cart",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_cart_item(
    item: CartDeleteItem = Body(...),
    user: "User" = Depends(required_roles([UserRoles.CLIENT])),
    cart_item_orchestrator: "CartItemOrchestrator" = Depends(
        get_cart_item_orchestrator
    ),
) -> None:
    await cart_item_orchestrator.delete_item(user_id=user.id, data=item)


@router.delete(
    "/items",
    summary="Clear cart",
    description="Remove all items from the user's shopping cart",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def clear_cart(
    user: "User" = Depends(required_roles([UserRoles.CLIENT])),
    cart_item_orchestrator: "CartItemOrchestrator" = Depends(
        get_cart_item_orchestrator
    ),
) -> None:
    await cart_item_orchestrator.clear_cart(user_id=user.id)
