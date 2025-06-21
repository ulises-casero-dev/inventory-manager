from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from src.enums import UserRole, Sector


class UserBase(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(..., description="User email address")
    sector: Sector = Field(..., description="User sector")
    active: bool = Field(True, description="Indicates if the user is active or not")
    role: UserRole = Field(..., description="User rol")

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=20)
    email: Optional[EmailStr] = Field(description="User email address")
    sector: Optional[Sector] = Field(description="User sector")
    active: Optional[bool] = Field(description="Indicates if the user is active or not")
    role: Optional[UserRole] = Field(description="User rol")

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True