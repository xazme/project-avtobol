import json
from uuid import UUID
from pydantic import BaseModel, model_validator


class CarBrandBase(BaseModel):
    name: str


class CarBrandCreate(CarBrandBase):
    pass

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class CarBrandUpdate(CarBrandBase):
    pass


class CarBrandResponse(CarBrandBase):
    id: UUID
    picture: str

    class Config:
        from_attributes = True
        validate_by_name = True
