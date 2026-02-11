import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field

class PurchaseBase(BaseModel):
    supplier_id: int = Field(gt=0)
    total_price: Decimal = Field(gt=0)
