from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint
from src.database.database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Numeric(10, 2), nullable=False, default=0)
    available = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    category = relationship("Category", back_populates="products")
    stock = relationship("Stock", back_populates="products", uselist=False)
    stock_movements = relationship("StockMovement", back_populates='products')
    product_suppliers = relationship("ProductSupplier", back_populates="products", cascade="all, delete-orphan")
    purchase_items = relationship("PurchaseItem", back_populates="product")

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_positive"),
    )