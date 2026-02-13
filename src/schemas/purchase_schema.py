import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import date

class PurchaseBase(BaseModel):
    supplier_id: int = Field(gt=0)
    total_price: Decimal = Field(gt=0)

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseUpdate(BaseModel):
    supplier_id: Optional[int] = Field(default=None, gt=0)
    total_price: Optional[Decimal] = Field(default=None, gt=0)

class PurchaseResponse(PurchaseBase):
    id: int
    date: date

    class Config:
        from_attributes = True