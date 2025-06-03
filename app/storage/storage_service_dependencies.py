from app.core import settings
from .storage_service import StorageService


storage_service = StorageService(
    bucket_name="avtobol",
    access_key=settings.minio.minio_access,
    secret_key=settings.minio.minio_secret,
    endpoint_url=f"{settings.minio.minio_url}",
)


def get_storage_service():
    return storage_service
