from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from src.database.database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Numeric(10,2))
    available = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    min_stock = Column(Integer, default=10)
    
    category = relationship("Category", back_populates="products")
    stock = relationship("Stock", back_populates="products", uselist=False)
    stock_movemetn = relationship("StockMovement", back_populates='products')

