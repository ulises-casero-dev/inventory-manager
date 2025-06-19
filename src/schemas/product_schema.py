from typing import Optional
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=4, max_length=50)
    description: Optional[str] = Field(min_length=15, max_length=250)
    price: float = Field(ge=0)
    category_id: int = Field(gt=0)
    #stock: int crear un modelo para el stock

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(min_length=4, max_length=50)
    description: Optional[str] = Field(min_length=15, max_length=250)
    price: Optional[float] = Field(gt=0)
    category_id: Optional[int] = Field(gt=0)

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True