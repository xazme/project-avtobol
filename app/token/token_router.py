from typing import TYPE_CHECKING
from uuid import UUID
from fastapi import APIRouter, Query, Depends, status
from app.core import settings
from .token_dependencies import get_token_handler
from .token_schema import TokenResponse

if TYPE_CHECKING:
    from .token_handler import TokenHandler

router = APIRouter(prefix=settings.api.token_prefix, tags=["Tokens"])


@router.get(
    "/all",
    summary="Get all tokens",
    description="Retrieve a list of all authentication tokens in the system",
    status_code=status.HTTP_200_OK,
    response_model=list[TokenResponse],
)
async def get_all_tokens(
    token_handler: "TokenHandler" = Depends(get_token_handler),
) -> list[TokenResponse]:
    tokens = await token_handler.get_all_tokens()
    return [TokenResponse.model_validate(token) for token in tokens]


@router.delete(
    "/",
    summary="Delete user tokens",
    description="Delete all authentication tokens for a specific user",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_tokens(
    user_id: UUID = Query(...),
    token_handler: "TokenHandler" = Depends(get_token_handler),
) -> dict[str, str]:
    await token_handler.delete_tokens_by_user_id(id=user_id)
