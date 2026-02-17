from sqlalchemy import Column, Boolean, String, Integer
from sqlalchemy.orm import relationship
from src.database.database import Base

class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), index=True, nullable=False)
    email = Column(String(100), nullable=True, unique=True)
    phone = Column(String(12), nullable=True)
    active = Column(Boolean, default=True, nullable=False)

    product_suppliers = relationship("ProductSupplier", back_populates="supplier", cascade="all, delete-orphan")
    purchases = relationship("Purchase", back_populates="supplier")