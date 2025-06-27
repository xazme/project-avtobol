from pydantic import BaseModel
from pydantic import EmailStr


class AuthCredentials(BaseModel):
    phone_number: str
    password: str
