from enum import Enum


class Tokens(Enum):
    SIGNIN: str = "sign-in"
    REGISTER: str = "register"
    ACCESS: str = "access"
    REFRESH: str = "refresh"
