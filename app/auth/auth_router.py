from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, Response, Form
from app.user import UserResponce
from app.token import (
    TokenResponse,
    Tokens,
    get_token_handler,
)
from app.shared import Roles
from .auth_dependencies import (
    AuthHandler,
    get_auth_handler,
    # register_user,
    # user_from_refresh_token,
)
from .auth_helper import create_token_response

if TYPE_CHECKING:
    from app.token import TokenHandler
    from app.user import User


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/sign-in")
async def auth(
    response: Response,
    username: str = Form(strict=True),
    password: str = Form(strict=True),
    auth_handler: "AuthHandler " = Depends(get_auth_handler),
    token_handler: "TokenHandler" = Depends(get_token_handler),
) -> TokenResponse:
    user = await auth_handler.sign_in(
        username=username,
        password=password,
    )
    token = await create_token_response(
        mode=Tokens.SIGNIN,
        user=user,
        token_handler=token_handler,
        response=response,
    )
    return TokenResponse.model_validate(token)


# @router.post("/register")
# async def register(
#     response: Response,
#     user: "User" = Depends(register_user),
#     token_handler: "TokenHandler" = Depends(get_token_handler),
# ):
#     token = await create_token_response(
#         mode=Tokens.REGISTER,
#         response=response,
#         user=user,
#         token_handler=token_handler,
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
#     token_handler: "TokenHandler" = Depends(get_token_handler),
# ):

#     access_token = token_handler.manager.generate_access_token(data=user_data)

#     return TokenResponse(
#         user_id=user.id,
#         access_token=access_token,
#     )
