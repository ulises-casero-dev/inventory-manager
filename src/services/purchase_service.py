from sqlalchemy.orm import Session
from src.models.purchase_model import Purchase
from src.schemas.purchase_schema import PurchaseUpdate, PurchaseCreate, PurchaseResponse
from src.services.stock_service import get_stock_by_prodcut_id

def get_all_purchases(db: Session):
    return db.query(Purchase).all()

def get_purchase_by_id(db: Session, id: int):
    return db.get(Purchase, id)
    
def create_purchase(db: Session, purchase_data: PurchaseCreate):
    try:
        #Obtener prodcuto importando get

 #       product = db.get(Product, id)
  #      if not product:
   #         return None

        #Obtener stock del producto en stoc


        stock = get_stock_by_prodcut_id(purchase_data.)
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


def purchase(db: Session, id: int, purchase_quantity: int):
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

