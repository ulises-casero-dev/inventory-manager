from sqlalchemy.orm import Session
from src.models.purchase_model import Purchase
from src.schemas.purchase_schema import PurchaseUpdate, PurchaseCreate, PurchaseResponse


def get_all_purchases(db: Session):
    return db.query(Purchase).all()

def get_purchase_by_id(db: Session, id: int):
    return db.get(Purchase, id)
    
def create_purchase(db: Session, purchase_data: PurchaseCreate):
    new_purchase = Purchase(**purchase_data.model_dump())
    
    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)

    return new_purchase

def update_purchase(db: Session, id: int, purcahse_data: PurchaseUpdate):
    purchase = db.get(Purchase, id)
    if not purchase:
        return None
    update_data = purcahse_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(purchase, key, value)

    db.commit()
    db.refresh(purchase)
    return purchase

def cancel_purchase(db: Session, id: int):
    purchase= db.get(Purchase, id)
    if not purchase:
        return None
    purchase.canceled = True
    
    db.commit()
    return purchase
