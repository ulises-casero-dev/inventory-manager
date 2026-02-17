from typing import Optional
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(...,min_length=4)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: str = Field(...,min_length=4)

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True