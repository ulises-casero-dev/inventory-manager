from sqlalchemy.orm import Session
from src.models.order_model import Order
from src.schemas.order_schema import OrderCreate, OrderUpdate

def get_all_orders(db: Session):
    return db.query(Order).all()

def get_order_by_id(db: Session, id: int):
    return db.get(Order, id)
    
def create_order(db: Session, order_data: OrderCreate):
    new_order = Order(**order_data.model_dump())
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

def update_order(db: Session, id: int, order_data: OrderUpdate):
    order = db.get(Order, id)
    if not order:
        return None
    update_data = order_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order

def cancel_order(db: Session, id: int):
    order = db.get(Order, id)
    if not order:
        return None
    order.canceled = True
    
    db.commit()
    return order
