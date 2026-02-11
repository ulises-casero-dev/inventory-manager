from sqlalchemy import Column, Boolean, ForeignKey, Integer, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from src.database.database import Base

class ProductSupplier(Base):
    __tablename__ = 'products_suppliers'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    is_preferred = Column(Boolean, default=False)
    active = Column(Boolean, default=True)

    __table_args__ = (UniqueConstraint("product_id", "supplier_id", name="uq_product_supplier"),)

    supplier = relationship("Supplier", back_populates="product_suppliers")
    product = relationship("Product", back_populates="product_suppliers")
