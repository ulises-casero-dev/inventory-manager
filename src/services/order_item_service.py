from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.order_item_model import OrderItem
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
    new_item = OrderItem(**item_data.model_dump())
    try:
        new_item.subtotal = new_item.quantity * new_item.unit_price
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
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