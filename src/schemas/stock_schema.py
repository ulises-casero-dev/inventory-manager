from typing import Optional
from pydantic import BaseModel, Field

class StockBase(BaseModel):
    quantity: int = Field(...,ge=0)
    product_id: int = Field(...,ge=0)
    min_quantity: int = Field(...,ge=10)

class StockCreate(StockBase):
    pass

class StockUpdate(BaseModel):
    quantity: Optional[int]= Field(default=None,ge=0)
    min_quantity: Optional[int] = Field(default=None,ge=10)

class StockResponse(StockBase):
    id: int

    class Config:
        from_attributes = True
