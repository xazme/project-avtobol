from pydantic import BaseModel


class StorageResponse(BaseModel):
    url: str


class StorageResponsePreview(BaseModel):
    list_of_files: list[str]
