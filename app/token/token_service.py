import jwt
from datetime import datetime, timedelta
from jwt.exceptions import (
    InvalidSignatureError,
    ExpiredSignatureError,
    DecodeError,
    InvalidAlgorithmError,
    ImmatureSignatureError,
    InvalidAudienceError,
)
from app.shared import ExceptionRaiser
from .token_enum import Tokens
from .token_types import AccessToken, RefreshToken


class TokenService:
    """TOKEN SERVICE"""

    def __init__(
        self,
        alogrithm,
        expire_days,
        expire_minutes,
        access_public_key,
        refresh_public_key,
        access_private_key,
        refresh_private_key,
    ):
        self.alogrithm = alogrithm
        self.expire_days = expire_days
        self.expire_minutes = expire_minutes
        self.access_public_key = access_public_key
        self.refresh_public_key = refresh_public_key
        self.access_private_key = access_private_key
        self.refresh_private_key = refresh_private_key

    def generate_access_token(self, data: dict) -> AccessToken:
        token = self.__encode(
            data=data,
            algorithm=self.alogrithm,
            private_key=self.access_private_key,
            expire_minutes=self.expire_minutes,
        )
        return AccessToken(token)

    def generate_refresh_token(self, data: dict) -> RefreshToken:
        token = self.__encode(
            data=data,
            algorithm=self.alogrithm,
            private_key=self.refresh_private_key,
            expire_days=self.expire_days,
        )
        return RefreshToken(token)

    def decode(
        self,
        token: str,
        type: Tokens,
    ) -> dict:

        key = (
            self.access_public_key if type == Tokens.ACCESS else self.refresh_public_key
        )

        try:
            data = jwt.decode(jwt=token, algorithms=[self.alogrithm], key=key)
        except ExpiredSignatureError:
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="Истёкший токен",
            )
        except InvalidSignatureError:
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="Неверная подпись токена",
            )
        except DecodeError:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Ошибка декодирования токена",
            )
        except InvalidAlgorithmError:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Неверный алгоритм подписи токена",
            )
        except ImmatureSignatureError:
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="Токен ещё не действителен",
            )
        except InvalidAudienceError:
            ExceptionRaiser.raise_exception(
                status_code=401,
                detail="Неверная аудитория токена",
            )
        except Exception:
            ExceptionRaiser.raise_exception(
                status_code=400,
                detail="Неизвестная ошибка обработки токена",
            )
        return data

    def __encode(
        self,
        data: dict,
        algorithm: str,
        private_key: str,
        expire_minutes: int | None = None,
        expire_days: int | None = None,
    ) -> str:
        now = datetime.utcnow()

        if expire_minutes:
            exp = now + timedelta(minutes=expire_minutes)
        else:
            exp = now + timedelta(days=expire_days)

        data_to_encode = data.copy()
        data_to_encode.update(
            exp=exp,
            iat=now,
        )

        return jwt.encode(
            payload=data_to_encode,
            key=private_key,
            algorithm=algorithm,
        )
