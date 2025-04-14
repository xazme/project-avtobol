from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from .token_service import TokenService
from app.core import settings
from app.token import Tokens

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.auth.access_token_url)


def get_token_service() -> TokenService:
    return TokenService(
        alogrithm=settings.auth.algorithm,
        expire_days=settings.auth.expire_days,
        expire_minutes=settings.auth.expire_days,
        access_private_key=settings.auth.access_private_key,
        access_public_key=settings.auth.access_public_key,
        refresh_private_key=settings.auth.refresh_private_key,
        refresh_public_key=settings.auth.refresh_public_key,
    )


def get_access_token(token: str = Depends(oauth2_scheme)) -> str:
    return token


def get_refresh_token(request: Request) -> str:
    return request.cookies.get(str(Tokens.REFRESH))
