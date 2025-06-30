from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class StockMovementBase(BaseModel):
    product_id: int = Field(gt=0)
    change: int
    movement_type: str = Field(min_length=5, max_length=15)
    created_at: datetime = Field(gt=datetime.today)

class StockMovementCreate(StockMovementBase):
    pass

class StockMovementUpdate(BaseModel):
    change: Optional[int]
    movement_type: Optional[str] = Field(min_length=5, max_length=15)

class StockMovementResponse(StockMovementBase):
    id: int

    class Config:
        from_atributes = True