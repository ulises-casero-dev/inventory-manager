from typing import Optional
from pydantic import BaseModel, Field

class StockBase(BaseModel):
    quantity: int = Field(ge=0)
    product_id: int = Field(ge=0)

class StockCreate(StockBase):
    pass

class StockUpdate(BaseModel):
    quantity: int= Field(ge=0)

class StockResponse(StockBase):
    id: int

    class Config:
        from_attributes = True
