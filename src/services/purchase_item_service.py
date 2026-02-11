from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.stock_model import Stock
from src.models.product_model import Product
from src.services.product_service import product_purchase
from src.schemas.order_item_schema import OrderItemCreate, OrderItemUpdate

def get_items_by_order_id(db: Session, id: int):
    try:
        return db.query(OrderItem).filter(OrderItem.order_id == id).all()
    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None

def get_item_by_id(db: Session, id: int):
    try:
        return db.get(OrderItem, id)
    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None

def create_order_item(db: Session, item_data: OrderItemCreate):
    order = db.query(Order).filter(Order.id == item_data.order_id).first()
    if not order:
        raise Exception('Order not found')
    
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise Exception('Product not found')

    stock_available = product_purchase(db, item_data.product_id, item_data.quantity)
    if not stock_available:
        raise Exception('Stock no aviable for this amount')
    

    try:
        new_item = OrderItem(**item_data.model_dump())
        new_item.subtotal = new_item.quantity * new_item.unit_price
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        db.refresh()
        return(new_item)
    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None

def update_order_item(db: Session, id: int, item_data: OrderItemUpdate):
    try:
        order_item = db.get(OrderItem, id)
        if not order_item:
            return None

        update_data = item_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(order_item, key, value)
        
        if 'quantity' in update_data or 'unit_price' in update_data:
            order_item.subtotal = order_item.quantity * order_item.unit_price
        
        db.commit()
        db.refresh(order_item)
        return order_item
    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None

def cancel_order_item(db: Session, id: int):
    try:
        order_item = db.get(OrderItem, id)
        if not order_item:
            return None
        
        order_item.canceled = True
        db.commit()
        db.refresh(order_item)
        return order_item
    except SQLAlchemyError as e:
        db.rollback()
        print(f'Database error: {e}')
        return None
    
def add_item_order(db: Session, items_data: List[OrderItemCreate]):
    created_items = []
    for item_data in items_data:
        item = create_order_item(db, item_data)
        if not item:
            return None
        created_items.append(item)
    return created_items