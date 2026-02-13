from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.services.purchase_service import (
    get_all_orders as get_all_orders_service,
    get_order_by_id as get_order_by_id_service,
    create_order as create_order_service,
    update_order as update_order_service,
    cancel_order as cancel_order_service
)

order_router = APIRouterorder_item_router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@order_router.get('/orders', status_code=200, response_model=List[OrderResponse], response_description='List of orders')
def get_orders(db: Session = Depends(get_db)):
    orders = get_all_orders_service(db)
    if not orders: 
       raise HTTPException(status_code=404, detail="Orders not found")
    return orders

@order_router.get('/orders/{id}', status_code=200, response_model=OrderResponse, summary="Get a order by id", response_description='Returns a order if it exists')
def get_order_by_id(id: int, db: Session = Depends(get_db)):
    order = get_order_by_id_service(db, id)
    if not order:
        return []
    return order

@order_router.post('/orders', status_code=201, response_model=OrderResponse, summary='Create a new order', response_description='Returns the created order')
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    new_order = create_order_service(db, order_data)
    return new_order

@order_router.put('/orders/{id}', status_code=200, response_model=OrderResponse, summary='', response_description='')
def update_order(id: int, order_data: OrderUpdate, db: Session = Depends(get_db)):
    order_updated = update_order_service(db, id, order_data)
    if not order_updated:
        raise HTTPException(status_code=404, detail='Order not found')
    return order_updated

@order_router.delete('/orders/{id}', status_code=200, response_model=OrderResponse, summary='', response_description='')
def cancel_order(id: int, db: Session = Depends(get_db)):
    order = get_order_by_id_service(db, id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    if order.canceled:
        raise HTTPException(status_code=400, detail="Order is already canceled")
    
    order = cancel_order_service(db, id)
    return order