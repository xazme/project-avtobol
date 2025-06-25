from fastapi import Request, Response
from app.core.config import settings


async def clear_cookies(request: Request, call_next):
    response: Response = await call_next(request)

    if response.status_code in [401, 403]:
        response.delete_cookie(
            key=settings.auth.refresh_token_key,
            httponly=True,
            secure=True,
            samesite="lax",
        )
    return response
