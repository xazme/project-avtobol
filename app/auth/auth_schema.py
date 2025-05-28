from pydantic import BaseModel
from pydantic import EmailStr


class AuthCredentials(BaseModel):
    email: EmailStr
    password: str
