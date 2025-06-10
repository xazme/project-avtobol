from fastapi import APIRouter, Depends, Query, status, UploadFile
from app.core.config import settings
from .storage_service import StorageService
from .storage_service_dependencies import get_storage_service
from .storage_schema import StorageResponse, StorageResponsePreview

router = APIRouter(prefix="/storage", tags=["S3"])


@router.get(
    "/",
    summary="Generate presigned url.",
    response_model=StorageResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_presigned_url(
    filename: str = Query(...),
    content_type: str = Query(...),
    storage_service: StorageService = Depends(get_storage_service),
) -> StorageResponse:
    url: str = await storage_service.get_presigned_upload_url(
        filename=filename,
        content_type=content_type,
    )
    return StorageResponse(url=url)


@router.post(
    "/",
    summary="Send files to MinIO storage.",
    response_model=StorageResponsePreview,
    status_code=status.HTTP_200_OK,
)
async def create_files(
    files: list[UploadFile],
    storage_service: StorageService = Depends(get_storage_service),
) -> StorageResponsePreview:
    list_of_files = []
    for file in files:
        list_of_files.append(await file.read())

    filenames: list[str] = await storage_service.create_files(
        list_of_files=list_of_files
    )
    return StorageResponsePreview(list_of_files=filenames)


# также и для удаления. просто поверьте
