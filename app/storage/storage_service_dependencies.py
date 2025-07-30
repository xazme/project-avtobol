from app.core import settings
from .storage_handler import StorageHandler

storage_handler = StorageHandler(
    bucket_name="razborka",
    access_key=settings.minio.minio_access,
    secret_key=settings.minio.minio_secret,
    endpoint_url=f"http://{settings.minio.minio_url}",
)


def get_storage_handler():
    return storage_handler
