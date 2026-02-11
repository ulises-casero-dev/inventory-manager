from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.order_item_schema import OrderItemCreate,OrderItemUpdate, OrderItemResponse
from src.services.purchase_item_service import (
    get_items_by_order_id as get_items_by_order_id_service,
    get_item_by_id as get_item_by_id_service,
    update_order_item as update_order_item_service,
    cancel_order_item as cancel_order_item_service,
    add_item_order as add_item_order_service
)

order_item_router = APIRouter(
    prefix="/order_items",
    tags=["Order Items"]
)

@order_item_router.get('/order_items/by_order/{order_id}', status_code=200, response_model=List[OrderItemResponse], summary='Get all order items by order id', response_description='Returns a list of items that belong to the specified order')
def get_items_by_order_id(order_id: int, db: Session = Depends(get_db)):
    order_items = get_items_by_order_id_service(db, order_id)
    if not order_items:
        raise HTTPException(status_code=404, detail='Items for the specified order not found')
    return order_items

@order_item_router.get('/order_items/{id}', status_code=200, response_model=OrderItemResponse, summary='Get an order item by id', response_description='Returns a single order item if it exists')
def get_item_by_id(id: int, db: Session = Depends(get_db)):
    item = get_item_by_id_service(db, id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    return item

@order_item_router.post('/order_items',status_code=201, response_model=List[OrderItemResponse], summary='Create a new order items', response_description='Creates a new items and associates them with an order')
def create_items(items_data: List[OrderItemCreate], db: Session =Depends(get_db)):
    new_item_list = add_item_order_service(db, items_data)
    if not new_item_list:
        raise HTTPException(status_code=400, detail='Failed to create items')
    return new_item_list

@order_item_router.put('/order_items/{id}', status_code=200, response_model=OrderItemResponse, summary='Update an existing order item', response_description='Updates the fields of an existing order item and returns the updated record')
def update_order_item(id: int, item_data: OrderItemUpdate, db: Session = Depends(get_db)):
    order_item_updated = update_order_item_service(db, id, item_data)
    if not order_item_updated:
        raise HTTPException(status_code=404, detail='Order item not faund')
    return order_item_updated

@order_item_router.delete('/order_items/{id}', status_code=200, response_model=OrderItemResponse, summary='Cancel an order item', response_description='Marks the item as canceled and returns the updated item')
def cancel_order_item(id: int, db: Session = Depends(get_db)):
    canceled_item = cancel_order_item_service(db, id)
    if not canceled_item:
        raise HTTPException(status_code=404, detail='Item not found')
    return canceled_item    
