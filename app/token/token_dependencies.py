from typing import TYPE_CHECKING
from fastapi import Depends, Response
from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import settings
from app.database import DBService
from app.shared import ExceptionRaiser
from .token_repository import TokenRepository
from .token_manager import TokenManager
from .token_handler import TokenHandler
from .token_model import Token
from .token_enums import TokenMode
from .token_schema import TokenCreate

if TYPE_CHECKING:
    from app.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.auth.access_token_url)
http_bearer = HTTPBearer(auto_error=False)


def get_token_handler(
    session: AsyncSession = Depends(DBService.get_session),
) -> TokenHandler:
    repository = TokenRepository(
        session=session,
        model=Token,
    )
    manager = TokenManager(
        alogrithm=settings.auth.algorithm,
        expire_days=settings.auth.expire_days,
        expire_minutes=settings.auth.expire_minutes,
        access_private_key=settings.auth.access_private_key,
        access_public_key=settings.auth.access_public_key,
        refresh_private_key=settings.auth.refresh_private_key,
        refresh_public_key=settings.auth.refresh_public_key,
    )
    return TokenHandler(
        repository=repository,
        manager=manager,
    )


def get_access_token(
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> HTTPAuthorizationCredentials:
    return token


def get_refresh_token(
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> HTTPAuthorizationCredentials:
    return token


async def create_token_response(
    mode: TokenMode,
    user: "User",
    token_handler: "TokenHandler",
    response: Response,
):
    user_data = {
        "id": str(user.id),
        "username": user.name,
    }
    access_token = token_handler.manager.generate_access_token(data=user_data)
    refresh_token = token_handler.manager.generate_refresh_token(data=user_data)

    token_data = TokenCreate(
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token,
    )

    if mode == TokenMode.REFRESH:
        token_data_for_refresh = TokenCreate(
            user_id=user.id,
            access_token=access_token,
        )
        token = await token_handler.update_access_token(
            user_id=user.id,
            data=token_data_for_refresh,
        )

    elif mode == TokenMode.SIGNIN:

        response.set_cookie(
            key=refresh_token,
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        await token_handler.delete_tokens_by_user_id(user_id=user.id)
        token = await token_handler.create_token(token_data)

    elif mode == TokenMode.REGISTER:
        response.set_cookie(
            key=refresh_token,
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        token: "Token" = await token_handler.create_token(data=token_data)

    if not token:
        ExceptionRaiser.raise_exception(
            status_code=500,
            detail="Token error",
        )
    return token


# def get_refresh_token(request: Request) -> str:
#     return request.cookies.get(str(Tokens.REFRESH))
