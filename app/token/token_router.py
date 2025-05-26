from uuid import UUID
from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, status
from app.core import settings
from .token_dependencies import get_token_handler
from .token_schema import TokenResponse


if TYPE_CHECKING:
    from .token_handler import TokenHandler

router = APIRouter(prefix=settings.api.token_prefix, tags=["Tokens"])


@router.get(
    "/all",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def get_all_tokens(
    token_handler: "TokenHandler" = Depends(get_token_handler),
):
    tokens = await token_handler.get_all_tokens()
    return [TokenResponse.model_validate(token) for token in tokens]


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_tokens(
    user_id: UUID,
    token_handler: "TokenHandler" = Depends(get_token_handler),
):
    result = await token_handler.delete_tokens_by_user_id(id=user_id)
    return {"msg": "success"}
