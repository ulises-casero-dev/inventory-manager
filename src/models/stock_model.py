from src.database.database import Base
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="stocks")
