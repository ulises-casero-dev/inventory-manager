from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal

class OrderItemBase(BaseModel):
    order_id: int = Field(gt=0, )
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(gt=0)
    
class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    order_id: Optional[int] = Field(gt=0, )
    product_id: Optional[int] = Field(gt=0)
    quantity: Optional[int] = Field(gt=0)
    unit_price: Optional[Decimal] = Field(gt=0)

class OrderItemResponse(OrderItemBase):
    id: int
    subtotal: Decimal

    class Config:
        from_attributes = True