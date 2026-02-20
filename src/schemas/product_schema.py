from typing import Optional
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(...,min_length=4, max_length=50)
    description: Optional[str] = Field(...,min_length=15, max_length=250)
    price: float = Field(...,gt=0)
    category_id: int = Field(...,gt=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None,min_length=4, max_length=50)
    description: Optional[str] = Field(default=None,min_length=15, max_length=250)
    price: Optional[float] = Field(default=None,gt=0)
    category_id: Optional[int] = Field(default=None,gt=0)

class ProductResponse(ProductBase):
    id: int
    available: bool

    class Config:
        from_attributes = True