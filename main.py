from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.user import user_router
from app.auth import auth_router
from app.core.config import settings
from app.database.db_service import DBService


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DBService.create_tables()
    yield
    await DBService.drop_tables()  # TODO turn off
    await DBService.dispose()


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(user_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )

# Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
