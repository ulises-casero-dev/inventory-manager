from src.database.database import Base
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True)
    quantity = Column(Integer)
    min_quantity = Column(Integer, default=10)

    products = relationship("Product", back_populates="stock")
