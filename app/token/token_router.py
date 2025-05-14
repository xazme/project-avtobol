from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, status
from app.core import settings
from app.shared import ExceptionRaiser
from .token_dependencies import get_token_handler
from .token_schema import TokenResponse, TokenCreate, TokenUpdate


if TYPE_CHECKING:
    from .token_handler import TokenHandler

router = APIRouter(prefix=settings.api.token_prefix, tags=["Tokens"])


@router.get(
    "/",
)
async def get_token(
    token_id: int,
    token_handler: "TokenHandler" = Depends(get_token_handler),
):
    token = await token_handler.get(id=token_id)
    return TokenResponse.model_validate(token)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
)
async def get_all_tokens(
    token_handler: "TokenHandler" = Depends(get_token_handler),
):
    tokens = await token_handler.get_all()
    return tokens


@router.post(
    "/",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def create_token(
    token_data: TokenCreate,
    token_handler: "TokenHandler" = Depends(get_token_handler),
):
    token = await token_handler.create(data=token_data)
    return TokenResponse.model_validate(token)


@router.put(
    "/",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def update_token(
    token_id: int,
    new_token_data: TokenUpdate,
    token_handler: "TokenHandler" = Depends(get_token_handler),
):
    upd_car_brand_data = await token_handler.update(id=token_id, data=new_token_data)
    return TokenResponse.model_validate(upd_car_brand_data)


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_token(
    token_id: int,
    token_handler: "TokenHandler" = Depends(get_token_handler),
):
    result = await token_handler.delete(id=token_id)
    return {"msg": "success"}
