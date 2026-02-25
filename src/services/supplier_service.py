from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.models.supplier_model import Supplier

from src.schemas.supplier_schema import SupplierResponse, SupplierCreate, SupplierUpdate

from src.exceptions.custom_exceptions import ConflictException

def get_all_suppliers(db: Session):
    return db.query(Supplier).all()

def grt_all_active_suppliers(db: Session):
    return db.query(Supplier).filter(Supplier.active).all()

def create_supplier(db: Session, supplier_data: SupplierCreate):
    if db.query(Supplier).filter(Supplier.name == supplier_data.name).first():
        raise ConflictException(
            message="Supplier with this name already exists.",
            error_code="SUPPLIER_ALREADY_EXISTS"
        )
    
    if db.query(Supplier).filter(Supplier.email == supplier_data.email).first():
        raise ConflictException(
            message="Supplier with this email already exists.",
            error_code="SUPPLIER_EMAIL_ALREADY_EXISTS"
        )

    try:
        new_supplier = Supplier(
            name=supplier_data.name,
            email=supplier_data.email,
            phone=supplier_data.phone
        )

        db.add(new_supplier)

        return new_supplier
    except SQLAlchemyError as e:
        pass