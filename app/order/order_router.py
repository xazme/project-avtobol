from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends
from app.auth import requied_roles
from app.shared import Roles
from .order_schema import OrderCreate, OrderResponse
from .order_dependencies import get_order_handler

if TYPE_CHECKING:
    from app.user import User
    from .order_handler import OrderHandler

router = APIRouter(prefix="/orders", tags=["suka"])


@router.post("/one", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    user: "User" = Depends(requied_roles([Roles.CLIENT])),
    order_handler: "OrderHandler" = Depends(get_order_handler),
):
    order = await order_handler.create_order(user_id=user.id, data=order_data)
    return OrderResponse.model_validate(order)


@router.post("/vse")
async def create_orders(
    order_data: OrderCreate,
    user: "User" = Depends(requied_roles([Roles.CLIENT])),
    order_handler: "OrderHandler" = Depends(get_order_handler),
):
    order = await order_handler.create_orders(user_id=user.id, data=order_data)
    # return await order
    return {"msg": "success"}


@router.get("/active")
async def get_active_user_orders(
    user: "User" = Depends(requied_roles([Roles.CLIENT])),
    order_handler: "OrderHandler" = Depends(get_order_handler),
):
    orders = await order_handler.get_active_user_orders(user_id=user.id)
    return [OrderResponse(order) for order in orders]


@router.get("/closed")
async def get_closed_user_orders(
    user: "User" = Depends(requied_roles([Roles.CLIENT])),
    order_handler: "OrderHandler" = Depends(get_order_handler),
):
    orders = await order_handler.get_closed_user_orders(user_id=user.id)
    return [OrderResponse(order) for order in orders]


@router.get("/denied")
async def get_denied_user_orders(
    user: "User" = Depends(requied_roles([Roles.CLIENT])),
    order_handler: "OrderHandler" = Depends(get_order_handler),
):
    orders = await order_handler.get_denied_user_orders(user_id=user.id)
    return [OrderResponse(order) for order in orders]
