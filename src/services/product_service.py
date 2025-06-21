from sqlalchemy.orm import Session
from src.models.product_model import Product
from src.schemas.product_schema import ProductUpdate, ProductCreate

def get_all_products(db: Session):
    return db.query(Product).filter(Product.available == True).all()

def create_product(db: Session, product_data: ProductCreate):
    new_product = Product(**product_data.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_product_by_id(db: Session, id: int):
    return db.get(Product, id)

def update_product(db: Session, id: int, product_data: ProductUpdate):
    product = db.get(Product, id)
    if not product:
        return None
    
    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

def desable_product(db: Session, id: int):
    product = db.get(Product, id)
    if not product:
        return None
    
    product.available = False
    db.commit()
    db.refresh(product)
    return product
