from pydantic import Field
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from src.database.database import Base
from typing import Optional, List
import datetime

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True)
    available = Column(Boolean, default=True)

    products = relationship("Product", back_populates="category")
