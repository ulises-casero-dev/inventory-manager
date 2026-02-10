from sqlalchemy import Column, Boolean, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship
from src.database.database import Base

class ProductSupplier(Base):
    __tablename__ = 'products_suppliers'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    unite_price = Column(Numeric(10, 2), nullable=False)
    is_preferred = Column(Boolean, default=False)
    active = Column(Boolean, default=True)

    supplier = relationship("Supplier", back_populates="suppliers")
    product = relationship("Product", back_populates="products")
    purchase = relationship("Purchase", back_populates="supplier")