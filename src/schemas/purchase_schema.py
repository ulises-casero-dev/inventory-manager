import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import date

from src.schemas.purchase_item_schema import PurchaseItemCreate

class PurchaseBase(BaseModel):
    supplier_id: int = Field(gt=0)
    purchase_items: list[PurchaseItemCreate]

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseUpdate(BaseModel):
    supplier_id: Optional[int] = Field(default=None, gt=0)
    total_price: Optional[Decimal] = Field(default=None, gt=0)

class PurchaseResponse(PurchaseBase):
    id: int
    total_price: Decimal
    date: date

    class Config:
        from_attributes = True