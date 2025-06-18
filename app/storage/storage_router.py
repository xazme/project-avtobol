from fastapi import APIRouter, Depends, File, Body, Query, status, UploadFile
from app.core.config import settings
from .storage_handler import StorageHandler
from .storage_service_dependencies import get_storage_handler
from .storage_schema import StorageResponse, StorageResponsePreview

router = APIRouter(prefix=settings.api.storage_prefix, tags=["Minio"])


@router.get(
    "/",
    summary="Generate presigned url.",
    response_model=StorageResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_presigned_url(
    filename: str = Query(...),
    content_type: str = Query(...),
    storage_service: StorageHandler = Depends(get_storage_handler),
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
    files: list[UploadFile] = File(...),
    storage_service: StorageHandler = Depends(get_storage_handler),
) -> StorageResponsePreview:
    list_of_files = []
    for file in files:
        list_of_files.append(await file.read())

    filenames: list[str] = await storage_service.create_files(
        list_of_files=list_of_files
    )
    return StorageResponsePreview(list_of_files=filenames)


@router.delete(
    "/",
    summary="Delete files from MinIO storage.",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
)
async def delete_files(
    filenames: list[str] = Body(...),
    storage_handler: StorageHandler = Depends(get_storage_handler),
) -> dict[str, str]:
    filenames: list[str] = await storage_handler.delete_files(list_of_files=filenames)
    return {"msg": "успешно удалено"}
