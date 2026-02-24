from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.stock_model import Stock
import src.models.purchase_item_model
import src.models.purchase_model
from src.models.purchase_model import Purchase
from src.models.purchase_item_model import PurchaseItem
from src.models.product_model import Product

from src.schemas.purchase_item_schema import PurchaseItemCreate, PurchaseItemUpdate, PurchaseItemResponse

from src.services.product_service import get_product_by_id
from src.services.purchase_service import get_purchase_by_id
from src.services.stock_service import get_stock_by_prodcut_id

from src.exceptions.custom_exceptions import ConflictException

def get_items_by_purchase_id(db: Session, id: int):
    try:
        return db.query(PurchaseItem).filter(PurchaseItem.purchase_id == id).all()
    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None

def get_item_by_id(db: Session, id: int):
    try:
        return db.get(PurchaseItem, id)
    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None

def create_purchase_item(db: Session, item_data: PurchaseItemCreate):

    purchase = get_purchase_by_id(item_data.purchase_id)
    if not purchase:
        raise ValueError('Purchase not found')
    
    product = get_product_by_id(item_data.product_id)
    if not product:
        raise ValueError('Product not found')

    if item_data.quantity > get_stock_by_prodcut_id(item_data.product_id):
        raise ConflictException(
            message="The item quantity cant be higher than the stock quantity.",
            error_code="LOWER_STOCK"
        )

    try:
        new_item = PurchaseItem(**item_data.model_dump())
        new_item.subtotal = new_item.quantity * new_item.unit_price

        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        return new_item
    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None

def update_purchase_item(db: Session, id: int, item_data: PurchaseItemUpdate):
    try:
        purchase_item = db.get(PurchaseItem, id)
        if not purchase_item:
            return None

        update_data = item_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(purchase_item, key, value)
        
        if 'quantity' in update_data or 'unit_price' in update_data:
            purchase_item.subtotal = purchase_item.quantity * purchase_item.unit_price
        
        db.commit()
        db.refresh(purchase_item)

        return purchase_item
    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None

def cancel_purchase_item(db: Session, id: int):
    try:
        purchase_item = db.get(PurchaseItem, id)
        if not purchase_item:
            return None
        
        purchase_item.canceled = True
        db.commit()
        db.refresh(purchase_item)
        return purchase_item
    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None
    
def add_item_purchase(db: Session, items_data: List[PurchaseItemCreate]):
    created_items = []
    for item_data in items_data:
        item = create_purchase_item(db, item_data)
        if not item:
            return None
        created_items.append(item)
    return created_items