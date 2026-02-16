from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.purchase_item_schema import PurchaseItemCreate, PurchaseItemUpdate, PurchaseItemResponse
from src.services.purchase_item_service import (
    get_items_by_purchase_id as get_items_by_purchase_id_service,
    get_item_by_id as get_item_by_id_service,
    update_purchase_item as update_purchase_item_service,
    cancel_purchase_item as cancel_purchase_item_service,
    create_purchase_item as create_purchase_item_service
)

purchase_item_router = APIRouter(
    prefix="/purchase_items",
    tags=["Purchase Items"]
)

@purchase_item_router.get('/purchase_items/by_order/{purchase_id}', status_code=200, response_model=List[PurchaseItemResponse], summary='Get all purchase items by order id', response_description='Returns a list of items that belong to the specified purhcase')
def get_items_by_order_id(purchase_id: int, db: Session = Depends(get_db)):
    purchase_items = get_items_by_purchase_id_service(db, purchase_id)
    if not purchase_items:
        raise HTTPException(status_code=404, detail='Items for the specified purchase not found')
    return purchase_items

@purchase_item_router.get('/purchase_items/{id}', status_code=200, response_model=PurchaseItemResponse, summary='Get an order item by id', response_description='Returns a single purchase item if it exists')
def get_item_by_id(id: int, db: Session = Depends(get_db)):
    item = get_item_by_id_service(db, id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    return item

@purchase_item_router.post('/purchase_items',status_code=201, response_model=List[PurchaseItemResponse], summary='Create new purchase items', response_description='Creates new items and associates them with an purchase')
def create_items(items_data: List[PurchaseItemCreate], db: Session =Depends(get_db)):
    #Crear un item por cada elemento de lista o enviar toda la lista,
    # el service recive solo un item, no una lista
    new_item_list = create_purchase_item_service(db, items_data)
    if not new_item_list:
        raise HTTPException(status_code=400, detail='Failed to create items')
    return new_item_list

@purchase_item_router.put('/purchase_items/{id}', status_code=200, response_model=PurchaseItemResponse, summary='Update an existing purchase item', response_description='Updates the fields of an existing purchase item and returns the updated record')
def update_purchase_item(id: int, item_data: PurchaseItemUpdate, db: Session = Depends(get_db)):
    purchase_item_updated = update_purchase_item_service(db, id, item_data)
    if not purchase_item_updated:
        raise HTTPException(status_code=404, detail='Purchase item not faund')
    return purchase_item_updated

@purchase_item_router.delete('/purchase_items/{id}', status_code=200, response_model=PurchaseItemResponse, summary='Cancel an purchase item', response_description='Marks the item as canceled and returns the updated item')
def cancel_purchase_item(id: int, db: Session = Depends(get_db)):
    canceled_item = cancel_purchase_item_service(db, id)
    if not canceled_item:
        raise HTTPException(status_code=404, detail='Item not found')
    return canceled_item    
