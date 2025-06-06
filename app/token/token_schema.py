from uuid import UUID
from pydantic import BaseModel


class TokenBase(BaseModel):
    user_id: UUID
    access_token: str | None = None
    refresh_token: str | None = None


class TokenCreate(TokenBase):
    pass


class TokenUpdate(TokenBase):
    pass


class TokenResponse(TokenBase):
    pass

    class Config:
        from_attributes = True
        validate_by_name = True
