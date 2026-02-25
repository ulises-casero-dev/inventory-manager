from typing import List
from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.services.stock_service import get_stock_by_prodcut_id
from src.services.product_service import get_product_by_id

from src.schemas.purchase_schema import PurchaseUpdate, PurchaseCreate, PurchaseResponse
from src.schemas.purchase_item_schema import PurchaseItemCreate, PurchaseItemUpdate, PurchaseItemResponse

from src.models.purchase_model import Purchase
from src.models.purchase_item_model import PurchaseItem

def get_all_purchases(db: Session):
    return db.query(Purchase).all()

def get_purchase_by_id(db: Session, id: int):
    return db.get(Purchase, id)


def create_purchase_item(db: Session, purchase_id: int, item_data: PurchaseItemCreate):
    purchase = get_purchase_by_id(purchase_id)
    if not purchase:
        raise ValueError('Purchase not found')

    #comprobar que el producto existe y esta activo
    product = get_product_by_id(item_data.product_id)
    if not product or not product.available:
        raise ValueError('Product not found')

    stock = get_stock_by_prodcut_id(product.id)
    if not stock:
        return None

    # COMPROBAR EXISTENCIA DE SUPPLIER Y SI ES ACTIVO
    #if

    try:
        new_item = PurchaseItem(
            purchase_id=purchase_id,
            product_id=product.id,
            quantity=item_data.quantity,
            unit_price=product.price,
            subtotal=item_data.quantity * product.price
        )

        db.add(new_item)

        return new_item
    except SQLAlchemyError as e:
        print(f'Database error: {e}')
        return None


def create_purchase(db: Session, purchase_data: PurchaseCreate):
    try:
        new_purchase = Purchase(
            supplier_id=purchase_data.supplier_id
        )

        db.add(new_purchase)

        db.flush()

        total_price: Decimal = Decimal(0)

        for item in purchase_data.purchase_items:
            new_item = create_purchase_item(db, new_purchase.id, item)
            total_price += new_item.subtotal

        new_purchase.total_price = total_price

        db.commit()
        db.refresh(new_purchase)

        return new_purchase

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
    purchase = db.get(Purchase, id)
    if not purchase:
        return None
    purchase.canceled = True
    
    db.commit()
    return purchase

