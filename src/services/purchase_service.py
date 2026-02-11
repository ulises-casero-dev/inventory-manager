from sqlalchemy.orm import Session
from src.models.purchase_model import Purchase
from src.schemas.order_schema import OrderCreate, OrderUpdate

def get_all_orders(db: Session):
    return db.query(Purchase).all()

def get_purchase_by_id(db: Session, id: int):
    return db.get(Purchase, id)
    
def create_Purchase(db: Session, purchase_data: OrderCreate):
    new_purchase = Purchase(**purchase_data.model_dump())
    
    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)
    return new_purchase

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
