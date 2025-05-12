# from typing import TYPE_CHECKING
# from fastapi import APIRouter, Depends, Response
# from app.user import UserResponce
# from app.token import (
#     TokenResponse,
#     Tokens,
#     get_token_service,
# )
# from app.shared import Roles
# from .auth_dependencies import (
#     authentificate_user,
#     register_user,
#     user_from_refresh_token,
# )
# from .auth_helper import requied_roles, create_token_response

# if TYPE_CHECKING:
#     from app.token import TokenService
#     from app.user import User


# router = APIRouter(tags=["Auth"], prefix="/auth")


# @router.post("/sign-in")
# async def auth(
#     response: Response,
#     user: "User" = Depends(authentificate_user),
#     token_service: "TokenService" = Depends(get_token_service),
# ) -> TokenResponse:

#     token = await create_token_response(
#         mode=Tokens.SIGNIN,
#         response=response,
#         user=user,
#         token_service=token_service,
#     )
#     return TokenResponse.model_validate(token)


# @router.post("/register")
# async def register(
#     response: Response,
#     user: "User" = Depends(register_user),
#     token_service: "TokenService" = Depends(get_token_service),
# ):

#     token = await create_token_response(
#         mode=Tokens.SIGNIN,
#         response=response,
#         user=user,
#         token_service=token_service,
#     )
#     return TokenResponse.model_validate(token)


# @router.get(
#     "/me",
#     response_model=UserResponce,
# )
# async def info(
#     user: "User" = Depends(requied_roles([Roles.WORKER, Roles.SEO, Roles.OWNER])),
# ):
#     return UserResponce.model_validate(user)


# @router.get(
#     "/refresh",
#     response_model=TokenResponse,
#     response_model_exclude_unset=True,
# )
# async def get_new_access(
#     user: "User" = Depends(user_from_refresh_token),
#     token_service: "TokenService" = Depends(get_token_service),
# ):

#     user_data = {
#         "id": user.id,
#         "username": user.name,
#     }

#     access_token = token_service.generate_access_token(data=user_data)

#     return TokenResponse(
#         user_id=user.id,
#         access_token=access_token,
#     )
