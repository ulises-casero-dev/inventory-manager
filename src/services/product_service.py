from sqlalchemy.orm import Session
from src.models.product_model import Product
from src.schemas.product_schema import ProductUpdate

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, id: int):
    return db.get(Product, id)

def update_product(db: Session, id: int, product_data: ProductUpdate):
    product = db.get(Product, id)
    if not product:
        return None
    
    update_data = product_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(prodcut, key, value)

    db.commit()
    db.refresh(product)
    return product