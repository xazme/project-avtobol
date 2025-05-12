# from fastapi import Depends, Request
# from fastapi.security import OAuth2PasswordBearer, HTTPBearer
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.core import settings
# from app.database import DBService
# from .token_service import TokenService
# from .token_enum import Tokens

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.auth.access_token_url)
# http_bearer = HTTPBearer(auto_error=False)


# def get_token_service(
#     session: AsyncSession = Depends(DBService.get_session),
# ) -> TokenService:
#     return TokenService(
#         session=session,
#         alogrithm=settings.auth.algorithm,
#         expire_days=settings.auth.expire_days,
#         expire_minutes=settings.auth.expire_days,
#         access_private_key=settings.auth.access_private_key,
#         access_public_key=settings.auth.access_public_key,
#         refresh_private_key=settings.auth.refresh_private_key,
#         refresh_public_key=settings.auth.refresh_public_key,
#     )


# def get_access_token(token: str = Depends(http_bearer)) -> str:
#     return token


# def get_refresh_token(token: str = Depends(http_bearer)) -> str:
#     return token


# # def get_refresh_token(request: Request) -> str:
# #     return request.cookies.get(str(Tokens.REFRESH))
