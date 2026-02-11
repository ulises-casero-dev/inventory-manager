from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class SupplierBase(BaseModel):
    name: str = Field(min_length=4, max_length=50)
    email: Optional[EmailStr] = Field(default=None,min_length=20, max_length=80)
    phone: Optional[str] = Field(default=None,min_length=8, max_length=11)

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=4, max_length=50)
    email: Optional[EmailStr] = Field(default=None, min_length=20, max_length=80)
    phone: Optional[str] = Field(default=None, min_length=8, max_length=11)
    active: Optional[bool] = Field(default=None)

class SupplierResponse(SupplierBase):
    id: int

    class Config:
        from_attributes: True