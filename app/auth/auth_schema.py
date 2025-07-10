from pydantic import BaseModel


class AuthCredentials(BaseModel):
    phone_number: str
    password: str
