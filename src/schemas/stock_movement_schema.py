from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class StockMovementBase(BaseModel):
    product_id: int = Field(gt=0)
    change: int
    movement_type: str = Field(min_length=5, max_length=15)

class StockMovementCreate(StockMovementBase):
    pass

class StockMovementUpdate(BaseModel):
    change: Optional[int]
    movement_type: Optional[str] = Field(min_length=5, max_length=15)

class StockMovementResponse(StockMovementBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True