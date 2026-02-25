from sqlalchemy import Column, Boolean, ForeignKey, Integer, Numeric, Date, func
from sqlalchemy.orm import relationship
from src.database.database import Base

class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    total_price = Column(Numeric(10,2), nullable=False)
    date = Column(Date, server_default=func.current_date(), nullable=False)

    supplier = relationship("Supplier", back_populates="purchases")
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan")
