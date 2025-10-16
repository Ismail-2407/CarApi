from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class CarBase(BaseModel):
    brand: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=100)
    year: int

    @field_validator('year')
    @classmethod
    def validate_year(cls, value) -> int:
        if not (1886 <= value <= datetime.now().year):
            raise ValueError(f"Year must be between 1886 and {datetime.now().year}")
        return value


class CarCreate(CarBase):
    pass


class CarRead(CarBase):
    id: int

