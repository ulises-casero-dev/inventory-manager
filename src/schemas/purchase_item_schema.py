from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal

class PurchaseItemBase(BaseModel):
    purchase_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    unit_price: Decimal = Field(gt=0)
    quantity: int = Field(gt=0)

class PurchaseItemCreate(PurchaseItemBase):
    pass

class PurchaseItemUpdate(BaseModel):
    quantity: Optional[int] = Field(default=None, gt=0)
class PurchaseItemResponse(PurchaseItemBase):
    id: int
    subt_total: Decimal

    class Config:
        from_attributes: True