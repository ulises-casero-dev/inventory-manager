from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.purchase_schema import PurchaseUpdate, PurchaseCreate, PurchaseResponse
from src.services.purchase_service import (
    get_all_purchases as get_all_purchases_service,
    get_purchase_by_id as get_purchase_by_id_service,
    create_purchase as create_purchase_service,
    update_purchase as update_purchase_service,
    cancel_purchase as cancel_purchase_service
)

purchase_router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)

@purchase_router.get('/purchases', status_code=200, response_model=List[PurchaseResponse], response_description='List of purchases')
def get_purchases(db: Session = Depends(get_db)):
    purchases = get_all_purchases_service(db)
    if not purchases:
       raise HTTPException(status_code=404, detail="Purchases not found")
    return purchases

@purchase_router.get('/purchases/{id}', status_code=200, response_model=PurchaseResponse, summary="Get a purchase by id", response_description='Returns a purchase if it exists')
def get_purchase_by_id(id: int, db: Session = Depends(get_db)):
    purchase = get_purchase_by_id_service(db, id)
    if not purchase:
        return []
    return purchase

@purchase_router.post('/purchases', status_code=201, response_model=PurchaseResponse, summary='Create a new purchase', response_description='Returns the created purchase')
def create_order(purchase_data: PurchaseCreate, db: Session = Depends(get_db)):
    new_order = create_purchase_service(db, purchase_data)
    return new_order

@purchase_router.put('/purchases/{id}', status_code=200, response_model=PurchaseResponse, summary='Updates a purchase by id', response_description='Returns the updated purhcase')
def update_purchase(id: int, purchase_data: PurchaseUpdate, db: Session = Depends(get_db)):
    purchase_updated = update_purchase_service(db, id, purchase_data)
    if not purchase_updated:
        raise HTTPException(status_code=404, detail='Purchase not found')
    return purchase_updated

@purchase_router.delete('/purchases/{id}', status_code=200, response_model=PurchaseResponse, summary='Cancel a purchase by id', response_description='Returns the canceled purhcase')
def cancel_order(id: int, db: Session = Depends(get_db)):
    purchase = get_purchase_by_id_service(db, id)
    if not purchase:
        raise HTTPException(status_code=404, detail='Purchase not found')
    if purchase.canceled:
        raise HTTPException(status_code=400, detail="Purchase is already canceled")
    
    canceled_purchase = cancel_purchase_service(db, id)
    return canceled_purchase