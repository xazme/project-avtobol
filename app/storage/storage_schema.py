from pydantic import BaseModel


class StorageResponse(BaseModel):
    url: str


class StorageToDelete(BaseModel):
    list_of_files: list[str]


class StorageResponsePreview(BaseModel):
    list_of_files: list[str]
