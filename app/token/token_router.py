# from typing import TYPE_CHECKING
# from fastapi import APIRouter, Depends, status
# from app.core import settings
# from app.shared import ExceptionRaiser
# from .token_dependencies import get_token_service
# from .token_schema import TokenResponse, TokenCreate, TokenUpdate


# if TYPE_CHECKING:
#     from .token_service import TokenService

# router = APIRouter(prefix=settings.api.token_prefix, tags=["Tokens"])


# @router.get(
#     "/",
# )
# async def get_token(
#     token_id: int,
#     token_service: "TokenService" = Depends(get_token_service),
# ):
#     token = await token_service.get(id=token_id)
#     if not token:
#         ExceptionRaiser.raise_exception(status_code=404)  # TODO
#     return TokenResponse.model_validate(token)


# @router.get(
#     "/all",
#     status_code=status.HTTP_200_OK,
# )
# async def get_all_tokens(
#     token_service: "TokenService" = Depends(get_token_service),
# ):
#     tokens = await token_service.get_all()
#     return tokens


# @router.post(
#     "/",
#     response_model=TokenResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def create_token(
#     token: TokenCreate,
#     token_service: "TokenService" = Depends(get_token_service),
# ):
#     data = token.model_dump()

#     token = await token_service.create(data=data)
#     if not token:
#         ExceptionRaiser.raise_exception(status_code=404, detail="naxyu sgonyai")  # TODO

#     return TokenResponse.model_validate(token)


# @router.put(
#     "/",
#     response_model=TokenResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def update_token(
#     token_id: int,
#     new_token_info: TokenUpdate,
#     token_service: "TokenService" = Depends(get_token_service),
# ):
#     data = new_token_info.model_dump(exclude_unset=True)
#     upd_car_brand_data = await token_service.update(id=token_id, new_data=data)
#     if not upd_car_brand_data:
#         ExceptionRaiser.raise_exception(status_code=404)  # TODO
#     return TokenResponse.model_validate(upd_car_brand_data)


# @router.delete(
#     "/",
#     response_model=None,
#     status_code=status.HTTP_200_OK,
# )
# async def delete_token(
#     token_id: int,
#     token_service: "TokenService" = Depends(get_token_service),
# ):
#     result = await token_service.delete(id=token_id)
#     if not result:
#         ExceptionRaiser.raise_exception(status_code=404)  # TODO
#     return {"msg": "success"}
