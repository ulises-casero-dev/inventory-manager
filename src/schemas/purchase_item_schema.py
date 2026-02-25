from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal

class PurchaseItemBase(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

class PurchaseItemCreate(PurchaseItemBase):
    pass

class PurchaseItemUpdate(BaseModel):
    quantity: Optional[int] = Field(default=None, gt=0)

class PurchaseItemResponse(PurchaseItemBase):
    id: int
    purchase_id: int
    unit_price: Decimal
    subtotal: Decimal

    class Config:
        from_attributes: True