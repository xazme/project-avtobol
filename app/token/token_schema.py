from uuid import UUID
from pydantic import BaseModel


class TokenBase(BaseModel):
    user_id: UUID


class TokenCreate(TokenBase):
    refresh_token: str | None = None


class TokenUpdate(TokenBase):
    pass


class TokenResponse(TokenBase):
    access_token: str | None = None

    class Config:
        from_attributes = True
        validate_by_name = True
