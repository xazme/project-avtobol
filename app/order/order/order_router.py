from typing import TYPE_CHECKING, Optional, List
from uuid import UUID
from fastapi import APIRouter, Body, Depends, status
from app.core import settings
from app.user.user_enums import UserRoles
from app.auth.auth_guard import required_roles
from .order_schema import (
    OrderCreate,
    OrderResponse,
    # OrderResponseExtended,
    # OrderUpdate,
    # OrderStatusUpdate,
)
from .order_dependencies import get_order_orchestrator

router = APIRouter(
    prefix=settings.api.order_prefix,
    tags=["Orders"],
)

if TYPE_CHECKING:
    from app.user import User
    from .order_orchestrator import OrderOrchestrator


@router.post(
    "/",
    summary="Create order",
    description="Create a new order from user's cart",
    status_code=status.HTTP_201_CREATED,
    response_model=OrderResponse,
)
async def create_order(
    order_data: OrderCreate = Body(...),
    user: "User" = Depends(required_roles(allowed_roles=[UserRoles.CLIENT])),
    order_orchestrator: "OrderOrchestrator" = Depends(get_order_orchestrator),
):
    order = await order_orchestrator.create_order(user_id=user.id, data=order_data)
    return OrderResponse.model_validate(order)


@router.post(
    "/",
    summary="Create order. Worker Access",
    description="Create a new order from user's cart",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(required_roles([UserRoles.WORKER]))],
    response_model=OrderResponse,
)
async def create_order_manually(
    order_data: OrderCreate = Body(...),
    product_articles: list[UUID] = Body(...),
    order_orchestrator: "OrderOrchestrator" = Depends(get_order_orchestrator),
):
    order = await order_orchestrator.create_order_manually(
        data=order_data,
        product_articles=product_articles,
    )
    return OrderResponse.model_validate(order)


# @router.get(
#     "/",
#     summary="Get user orders",
#     description="Retrieve all orders for the current user",
#     status_code=status.HTTP_200_OK,
#     response_model=list[OrderResponseExtended],
# )
# async def get_user_orders(
#     user: "User" = Depends(required_roles(allowed_roles=[UserRoles.CLIENT])),
#     order_orchestrator: "OrderOrchestrator" = Depends(get_order_orchestrator),
# ):
#     orders = await order_orchestrator.get_user_orders(user_id=user.id)
#     return [OrderResponseExtended.model_validate(order) for order in orders]


# @router.get(
#     "/{order_id}",
#     summary="Get order details",
#     description="Retrieve detailed information about a specific order",
#     status_code=status.HTTP_200_OK,
#     response_model=OrderResponseExtended,
# )
# async def get_order(
#     order_id: UUID,
#     user: "User" = Depends(required_roles(allowed_roles=[UserRoles.CLIENT])),
#     order_orchestrator: "OrderOrchestrator" = Depends(get_order_orchestrator),
# ):
#     order = await order_orchestrator.get_order(user_id=user.id, order_id=order_id)
#     return OrderResponseExtended.model_validate(order)


# @router.patch(
#     "/{order_id}",
#     summary="Update order",
#     description="Update order information (only for client)",
#     status_code=status.HTTP_200_OK,
#     response_model=OrderResponse,
# )
# async def update_order(
#     order_id: UUID,
#     update_data: OrderUpdate = Body(...),
#     user: "User" = Depends(required_roles(allowed_roles=[UserRoles.CLIENT])),
#     order_orchestrator: "OrderOrchestrator" = Depends(get_order_orchestrator),
# ):
#     updated_order = await order_orchestrator.update_order(
#         user_id=user.id, order_id=order_id, data=update_data
#     )
#     return OrderResponse.model_validate(updated_order)


# @router.patch(
#     "/{order_id}/status",
#     summary="Update order status",
#     description="Update order status (only for admin/manager)",
#     status_code=status.HTTP_200_OK,
#     response_model=OrderResponse,
# )
# async def update_order_status(
#     order_id: UUID,
#     status_data: OrderStatusUpdate = Body(...),
#     user: "User" = Depends(
#         required_roles(allowed_roles=[UserRoles.ADMIN, UserRoles.MANAGER])
#     ),
#     order_orchestrator: "OrderOrchestrator" = Depends(get_order_orchestrator),
# ):
#     updated_order = await order_orchestrator.update_order_status(
#         order_id=order_id, status_data=status_data
#     )
#     return OrderResponse.model_validate(updated_order)
