from datetime import datetime
from src.database.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

class StockMovement(Base):
    __tablename__ = 'stock_movements'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True, nullable=False)
    change = Column(Integer, nullable=False)
    movement_type = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    canceled = Column(Boolean, default=False, nullable=False)

    product = relationship('Product', back_populates='stock_movements')