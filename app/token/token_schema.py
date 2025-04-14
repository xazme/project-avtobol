from pydantic import BaseModel


class TokenShema(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    type: str = "Bearer"
