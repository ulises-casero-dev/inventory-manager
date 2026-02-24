from http.client import HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from src.schemas.stock_movement_schema import StockMovementCreate
from src.models.product_model import Product
from src.models.category_model import Category
from src.models.stock_model import Stock
from src.schemas.product_schema import ProductUpdate, ProductCreate
from src.exceptions.custom_exceptions import ConflictException

from src.services.stock_movement_service import create_movement

def get_all_products(db: Session):
    return db.query(Product).filter(Product.available == True).all()

def create_product(db: Session, product_data: ProductCreate):
    try:
        existing_product = db.query(Product).filter(Product.name == product_data.name).first()

        if existing_product:
            raise ConflictException(
                message="Product with this name already exists.",
                error_code="PRODUCT_ALREADY_EXISTS"
            )

        new_product = Product(**product_data.model_dump())       
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None

def get_product_by_id(db: Session, id: int):
    return db.get(Product, id)

def update_product(db: Session, id: int, product_data: ProductUpdate):
    product = db.get(Product, id)
    if not product:
        return None

    update_data = product_data.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] != product.name:
        existing_product = db.query(Product).filter(
            Product.name == update_data["name"],
            Product.id != id
        ).first()

        if existing_product:
            raise ConflictException(
                message="Product with this name already exists.",
                error_code="PRODUCT_ALREADY_EXISTS"
            )

    if "category_id" in update_data and update_data["category_id"] != product.category_id:
        existing_category = db.query(Category).filter(Category.id == update_data["category_id"]).first()

        if not existing_category:
            raise ConflictException(
                message="The selected category does not exists.",
                error_code="CATEGORY_NOT_EXISTS"
            )

        if not existing_category.available:
            raise ConflictException(
                message="The selected category is not available.",
                error_code="CATEGORY_NOT_AVAILABLE"
            )

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

def disable_product(db: Session, id: int):
    product = db.get(Product, id)
    if not product:
        return None

    if not product.available:
        raise ConflictException(
            message="This product is already disabled.",
            error_code="PRODUCT_ALREADY_DISABLED"
        )
    
    product.available = False
    db.commit()
    db.refresh(product)
    return product

def get_product_by_name(db: Session, product_name: str):
    try: 
        product = db.query(Product).filter(func.lower(Product.name) == product_name).first()
        return product is not None    
    except SQLAlchemyError as e:
        print(f'Database error: {e}')
        return None

def get_product_by_category(db: Session, category_id):
    products = db.query(Product).filter(Product.category_id == category_id).all()
    return products if products else None

def bulk_update_prices(db: Session, category_id, percentaje_incres: float):
    try:
        products_to_update = get_product_by_category(db, category_id)
        if not products_to_update:
            return None
        
        for product in products_to_update:
            product.price += (percentaje_incres * product.price) / 100

        db.commit()
        return(products_to_update)
    
    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None

def get_lower_stocks(db: Session):
    try:
        return db.query(Product).join(Stock).filter(Stock.quantity <= Stock.min_quantity).all()
    except SQLAlchemyError as e:
        print(f'Database error: {e}')
        return []
    
def product_purchase(db: Session, id: int, purchase_quantity: int):
    try:
        product = db.get(Product, id)
        if not product:
            return None
       
        stock = db.query(Stock).filter(Stock.product_id == id).first()
        if not stock:
            return None
        
        if stock.quantity < purchase_quantity:
            return None
        
        if stock.quantity < purchase_quantity:
            return None
        
        stock.quantity -= purchase_quantity
        
        movement_data = StockMovementCreate(
            product_id=id,
            change=-purchase_quantity,
            movemente_type='sale'
        )
        create_movement(db, movement_data)
        
        return stock

    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None
    

    