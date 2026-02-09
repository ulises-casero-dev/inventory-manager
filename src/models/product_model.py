from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from src.database.database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    available = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    category = relationship("Category", back_populates="products")
    stock = relationship("Stock", back_populates="products", uselist=False)
    stock_movements = relationship("StockMovement", back_populates='products')

    suppliers = relationship("ProductSupplier", back_populates="products",
                             cascade="all, delete-orphan")