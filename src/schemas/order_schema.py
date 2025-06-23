from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class OrderBase(BaseModel):
    date: datetime
    total: float = Field(gt=0)
    canceled: bool

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    total: Optional[int]
    canceled: Optional[bool]

class OrderResponse(OrderBase):
    id: int

    class Config:
        from_attributes = True