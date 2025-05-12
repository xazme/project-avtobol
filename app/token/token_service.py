# import jwt
# from datetime import datetime, timedelta
# from jwt.exceptions import (
#     InvalidSignatureError,
#     ExpiredSignatureError,
#     DecodeError,
#     InvalidAlgorithmError,
#     ImmatureSignatureError,
#     InvalidAudienceError,
# )
# from sqlalchemy import Select, Result
# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.shared import ExceptionRaiser, CRUDGenerator
# from .token_enum import Tokens
# from .token_model import Token
# from .token_types import AccessToken, RefreshToken


# class TokenService(CRUDGenerator):
#     """TOKEN SERVICE"""

#     def __init__(
#         self,
#         session: AsyncSession,
#         alogrithm: str,
#         expire_days: int,
#         expire_minutes: int,
#         access_public_key: str,
#         refresh_public_key: str,
#         access_private_key: str,
#         refresh_private_key: str,
#     ):
#         self.alogrithm = alogrithm
#         self.expire_days = expire_days
#         self.expire_minutes = expire_minutes
#         self.access_public_key = access_public_key
#         self.refresh_public_key = refresh_public_key
#         self.access_private_key = access_private_key
#         self.refresh_private_key = refresh_private_key
#         super().__init__(
#             session=session,
#             model=Token,
#         )

#     def generate_access_token(self, data: dict) -> AccessToken:
#         token = self.__encode(
#             data=data,
#             algorithm=self.alogrithm,
#             private_key=self.access_private_key,
#             expire_minutes=self.expire_minutes,
#         )
#         return AccessToken(token)

#     def generate_refresh_token(self, data: dict) -> RefreshToken:
#         token = self.__encode(
#             data=data,
#             algorithm=self.alogrithm,
#             private_key=self.refresh_private_key,
#             expire_days=self.expire_days,
#         )
#         return RefreshToken(token)

#     def decode(
#         self,
#         token: str,
#         type: Tokens,
#     ) -> dict:

#         key = (
#             self.access_public_key if type == Tokens.ACCESS else self.refresh_public_key
#         )

#         try:
#             data = jwt.decode(jwt=token, algorithms=[self.alogrithm], key=key)
#         except ExpiredSignatureError:
#             ExceptionRaiser.raise_exception(
#                 status_code=401,
#                 detail="Истёкший токен",
#             )
#         except InvalidSignatureError:
#             ExceptionRaiser.raise_exception(
#                 status_code=401,
#                 detail="Неверная подпись токена",
#             )
#         except DecodeError:
#             ExceptionRaiser.raise_exception(
#                 status_code=400,
#                 detail="Ошибка декодирования токена",
#             )
#         except InvalidAlgorithmError:
#             ExceptionRaiser.raise_exception(
#                 status_code=400,
#                 detail="Неверный алгоритм подписи токена",
#             )
#         except ImmatureSignatureError:
#             ExceptionRaiser.raise_exception(
#                 status_code=401,
#                 detail="Токен ещё не действителен",
#             )
#         except InvalidAudienceError:
#             ExceptionRaiser.raise_exception(
#                 status_code=401,
#                 detail="Неверная аудитория токена",
#             )
#         except Exception:
#             ExceptionRaiser.raise_exception(
#                 status_code=400,
#                 detail="Неизвестная ошибка обработки токена",
#             )
#         return data

#     async def get_token_by_owner(
#         self,
#         id: int,
#     ) -> DeclarativeBase | None:
#         stmt = Select(self.model).where(self.model.user_id == id)
#         result: Result = await self.session.execute(statement=stmt)
#         return result.scalar_one_or_none()

#     async def update_access_token(
#         self,
#         user_id: int,
#         new_data: dict,
#     ) -> DeclarativeBase | None:
#         token = await self.get_token_by_owner(id=user_id)

#         if token is None:
#             return None

#         for key, value in new_data.items():
#             setattr(token, key, value)

#         await self.session.commit()
#         await self.session.refresh(token)
#         return token

#     async def delete_token(self, user_id):
#         token = await self.get_token_by_owner(id=user_id)

#         if token is None:
#             return None

#         await self.session.delete(token)
#         await self.session.commit()
#         return True

#     async def get_access_token(
#         self,
#         token,
#     ) -> DeclarativeBase | None:
#         stmt = Select(self.model).where(self.model.access_token == token)
#         result: Result = await self.session.execute(statement=stmt)
#         return result.scalar_one_or_none()

#     async def get_refresh_token(
#         self,
#         token,
#     ) -> DeclarativeBase | None:
#         stmt = Select(self.model).where(self.model.refresh_token == token)
#         result: Result = await self.session.execute(statement=stmt)
#         return result.scalar_one_or_none()

#     def __encode(
#         self,
#         data: dict,
#         algorithm: str,
#         private_key: str,
#         expire_minutes: int | None = None,
#         expire_days: int | None = None,
#     ) -> str:
#         now = datetime.utcnow()

#         if expire_minutes:
#             exp = now + timedelta(minutes=expire_minutes)
#         else:
#             exp = now + timedelta(days=expire_days)

#         data_to_encode = data.copy()
#         data_to_encode.update(
#             exp=exp,
#             iat=now,
#         )

#         return jwt.encode(
#             payload=data_to_encode,
#             key=private_key,
#             algorithm=algorithm,
#         )
