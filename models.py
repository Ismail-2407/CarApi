from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class Car(Base):
    __tablename__ = "cars"
    
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


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


class CarUpdate(BaseModel):
    brand: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=100)
    year: int

    @field_validator('year')
    @classmethod
    def validate_year(cls, value) -> int:
        if not (1886 <= value <= datetime.now().year):
            raise ValueError(f"Year must be between 1886 and {datetime.now().year}")
        return value


class CarRead(CarBase):
    id: int
    created_at: datetime = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

