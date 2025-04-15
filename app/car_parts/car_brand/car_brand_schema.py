from pydantic import BaseModel


class CarBrand(BaseModel):
    id: int
    name: str
