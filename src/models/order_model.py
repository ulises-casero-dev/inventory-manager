from sqlalchemy import Column, Integer, Numeric, DateTime, Boolean
from sqlalchemy.orm import relationship
from src.database.database import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    total = Column(Numeric(10,2))
    canceled = Column(Boolean, default=False)

    items = relationship('OrderItem', back_populates='orders')
