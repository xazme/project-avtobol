from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends
from app.auth import requied_roles
from app.user import UserRoles
from app.cart import get_cart_handler
from .order_schema import OrderCreate, OrderResponse
from .order_dependencies import get_order_handler
from .order_enums import OrderStatuses

if TYPE_CHECKING:
    from app.user import User
    from app.cart import CartHandler
    from .order_handler import OrderHandler

router = APIRouter(prefix="/orders", tags=["suka"])


@router.post(
    "/ebe",
    response_model=OrderResponse,
)
async def create_order(
    order_data: OrderCreate,
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    cart_hander: "CartHandler" = Depends(get_cart_handler),
    order_handler: "OrderHandler" = Depends(get_order_handler),
):
    user_positions = await cart_hander.get_all_user_positions(user_id=user.id)
    order = await order_handler.create_order(
        user_id=user.id,
        user_positions=user_positions,
        data=order_data,
    )
    return OrderResponse.model_validate(order)


@router.get("/my-orders")
async def get_user_orders(
    status: OrderStatuses,
    user: "User" = Depends(requied_roles([UserRoles.CLIENT])),
    order_handler: "OrderHandler" = Depends(get_order_handler),
):
    orders = await order_handler.get_all_orders_by_user_id(
        user_id=user.id,
        status=status,
    )
    return [OrderResponse(order) for order in orders]
