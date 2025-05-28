from enum import Enum


class TokenMode(Enum):
    SIGNIN: str = "sign-in"
    REGISTER: str = "register"
    ACCESS: str = "access"
    REFRESH: str = "refresh"


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
